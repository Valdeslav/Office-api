from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView, get_object_or_404

from reservation.models import Reservation
from person.serializers import PersonSerializer

from .models import Room
from .serializers import RoomSerializer


class RoomView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class SingleRoomView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class FreeRoomView(APIView):
    def get(self, request, req_date):
        try:
            date = datetime.strptime(req_date, "%Y-%m-%d")
        except ValueError:
            return Response(
                {"error": "date does not match format '%Y-%m-%d'"},
                status=400
            )

        if date < datetime.today():
            return Response(
                {"error": "date should not be earlier than today"},
                status=400
            )

        rooms = Room.objects.all()
        available_rooms = []
        for room in rooms:
            taken_seats = Reservation.objects.filter(
                room=room,
                start_date__lte=date,
                end_date__gte=date
            ).count()
            if taken_seats < room.seats_num:
                available_rooms.append(room)

        serializer = RoomSerializer(available_rooms, many=True)

        return Response(
            {"available_rooms": serializer.data}
        )


class ReservInfoView(APIView):
    # what persons reserved room
    def get(self, request, number, req_date=0):
        room = get_object_or_404(Room.objects.all(), number=number)
        room_reservs = Reservation.objects.filter(room=room)

        if req_date:
            try:
                date = datetime.strptime(req_date, "%Y-%m-%d")
            except ValueError:
                return Response(
                    {"error": "date does not match format '%Y-%m-%d'"},
                    status=400
                )
            room_reservs = room_reservs.filter(start_date__lte=date, end_date__gte=date)

        persons = []
        for reserv in room_reservs:
            person = reserv.person
            persons.append(person)

        serializer = PersonSerializer(persons, many=True)
        return Response(
            {"number": number, "date": req_date, "persons": serializer.data}
        )
