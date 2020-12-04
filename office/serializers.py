from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    seats_num = serializers.IntegerField()

    def create(self, validated_data):
        return Room.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.seats_num = validated_data.get('seats_num', instance.seats_num)
        instance.save()
        return instance
