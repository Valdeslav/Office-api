from datetime import datetime

from rest_framework import serializers
from django.core.validators import MinValueValidator

from office.models import Room
from person.models import Person

from .models import Reservation


class ReservSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'room', 'start_date', 'end_date', 'person')

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError(
                {"end_date": "end_date must be greater than or equal to start_date"}
            )
        if datetime.today().date() > data['start_date']:
            raise serializers.ValidationError(
                {"start_date": "start_date must be greater than or equal to current date"}
            )
        return data
