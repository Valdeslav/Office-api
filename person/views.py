from datetime import datetime

from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from reservation.models import Reservation
from reservation.serializers import ReservSerializer

from .models import Person
from .serializers import PersonSerializer


class PersonView(APIView):
    def get(self, request, id=0):
        if id:
            person = get_object_or_404(Person.objects.all(), id=id)
            serializer = PersonSerializer(person)
            return Response({'person': serializer.data})

        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response({'persons': serializer.data})

    def post(self, request):
        person = request.data.get('person')
        serializer = PersonSerializer(data=person)
        if serializer.is_valid(raise_exception=True):
                person_saved = serializer.save()
        return Response(
            {'success': f"Person '{person_saved}' created successfully"}
        )

    def put(self, request, id=0):
        if not id:
            raise Http404
        saved_person = get_object_or_404(Person.objects.all(), id=id)
        data = request.data.get('person')
        serializer = PersonSerializer(instance=saved_person, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            person_saved = serializer.save()

        return Response(
            {"success": f"Person '{person_saved}' updated successfully"}
        )

    def delete(self, request, id=0):
        if not id:
            raise Http404

        person = get_object_or_404(Person.objects.all(), id=id)
        person.delete()
        return Response(
            {"message": f"Person with id '{id}' has been deleted"},
            status=204
        )


class ReservInformationView(APIView):
    # get reserved rooms for chosen person
    def get(self, request, pers_id, req_date=0):
        person = get_object_or_404(Person.objects.all(), id=pers_id)
        reservations = Reservation.objects.filter(person=person)

        if req_date:
            try:
                date = datetime.strptime(req_date, "%Y-%m-%d")
            except ValueError:
                return Response(
                    {"error": "date does not match format '%Y-%m-%d'"},
                    status=400
                )
            reservations = reservations.filter(start_date__lte=date, end_date__gte=date)

        data = ReservSerializer(reservations, partial=True, many=True).data

        for reserv in data:
            del reserv['id'], reserv['person']

        return Response({'person': PersonSerializer(person).data, 'rooms': data})
