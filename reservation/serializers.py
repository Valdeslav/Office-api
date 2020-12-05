from datetime import datetime

from rest_framework import serializers
from django.core.validators import MinValueValidator

from office.models import Room
from person.models import Person

from .models import Reservation


class ReservSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    start_date = serializers.DateField(
        validators=[

        ]
    )
    end_date = serializers.DateField()
    person = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({"end_date": "end_date must be greater than or equal to start_date"})
        if datetime.today().date() > data['start_date']:
            raise serializers.ValidationError({"start_date": "start_date must be greater than or equal to current date"})
        return data

    def create(self, validated_data):
        return Reservation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.room = validated_data.get('room', instance.room)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.person = validated_data.get('person', instance.person)
        instance.save()
        return instance

