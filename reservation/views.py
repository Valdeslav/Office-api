from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.http import Http404

from .models import Reservation
from .serializers import ReservSerializer


class ReservationView(APIView):
    def get(self, request, id=0):
        if id:
            reservation = get_object_or_404(Reservation.objects.all(), id=id)
            serializer = ReservSerializer(reservation)
            return Response({'reservation': serializer.data})

        reservations = Reservation.objects.all()
        serializer = ReservSerializer(reservations, many=True)
        return Response({'reservations': serializer.data})

    def post(self, request):
        reservation = request.data.get('reservation')
        serializer = ReservSerializer(data=reservation)
        if serializer.is_valid(raise_exception=True):
            reservations = Reservation.objects.filter()
            reservation_saved = serializer.save()
        return Response({'success': f"Reservation '{reservation_saved}' created successfully"})
