from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.http import Http404

from .models import Reservation
from .serializers import ReservSerializer


class ReservationView(APIView):
    def get(self, request, res_id=0):
        if res_id:
            reservation = get_object_or_404(Reservation.objects.all(), id=res_id)
            serializer = ReservSerializer(reservation)
            return Response({'reservation': serializer.data})

        reservations = Reservation.objects.all()
        serializer = ReservSerializer(reservations, many=True)
        return Response({'reservations': serializer.data})

    def post(self, request):
        reserv_json = request.data.get('reservation')
        serializer = ReservSerializer(data=reserv_json)

        if serializer.is_valid(raise_exception=True):
            reservation = serializer.save()

        return Response(reservation.save_reserv('create'))

    def put(self, request, res_id=0):
        if not res_id:
            raise Http404

        saved_reservation = get_object_or_404(Reservation.objects.all(), id=res_id)
        data = request.data.get('reservation')
        serializer = ReservSerializer(instance=saved_reservation, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            reservation = serializer.save()
        return Response(reservation.save_reserv('update'))

    def delete(self, request, res_id):
        reservation = get_object_or_404(Reservation.objects.all(), id=res_id)
        reservation.delete()
        return Response(
            {"message": f"Reservation with id '{res_id}' has been deleted"},
            status=204
        )
