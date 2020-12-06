from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.db.utils import IntegrityError
from django.http import Http404

from reservation.models import Reservation
from person.serializers import PersonSerializer

from .models import Room
from .serializers import RoomSerializer


class RoomView(APIView):
    def get(self, request, number=0):
        if number:
            room = get_object_or_404(Room.objects.all(), number=number)
            serializer = RoomSerializer(room)
            return Response({'room': serializer.data})

        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response({'rooms': serializer.data})

    def post(self, request):

        room = request.data.get('room')
        serializer = RoomSerializer(data=room)
        if serializer.is_valid(raise_exception=True):
            try:
                room_saved = serializer.save()
            except IntegrityError:
                return Response(
                    {'error': f"Room with number {room['number']} is already exist"},
                    status=409
                )

        return Response(
            {'success': f"Room '{room_saved}' created successfully"}
        )

    def put(self, request, number=0):
        if not number:
            raise Http404

        saved_room = get_object_or_404(Room.objects.all(), number=number)
        data = request.data.get('room')
        serializer = RoomSerializer(instance=saved_room, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            try:
                room_saved = serializer.save()
            except IntegrityError:
                return Response(
                    {f'error': f"Room with number {data['number']} is already exist"},
                    status=400
                )

        return Response(
            {"success": f"Room '{room_saved}' updated successfully"}
        )

    def delete(self, request, number=0):
        if not number:
            raise Http404
        room = get_object_or_404(Room.objects.all(), number=number)
        room.delete()
        return Response(
            {"message": f"Room with id '{number}' has been deleted"},
            status=204
        )


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
