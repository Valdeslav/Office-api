from django.db import models
from django.core.validators import MaxValueValidator


class Room(models.Model):
    number = models.PositiveIntegerField(db_index=True)
    seats_num = models.PositiveIntegerField(
        validators=[MaxValueValidator(30, message="Number of seats must be lower than 30"), ])

    class Meta:
        ordering = ('number',)


class Person(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)
