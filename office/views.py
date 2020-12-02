from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Room

class RoomView(APIView):
    def get(self, request, date):

