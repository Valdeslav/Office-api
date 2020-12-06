from datetime import datetime

from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView

from reservation.models import Reservation
from reservation.serializers import ReservSerializer

from .models import Person
from .serializers import PersonSerializer


class PersonView(ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class SinglePersonView(RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


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
