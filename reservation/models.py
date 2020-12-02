from django.db import models

from office.models import Room
from person.models import Person


class Reservation(models.Model):
    room = models.ForeignKey(Room, related_name="room", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        ordering = ('room',)

    def __str__(self):
        return f"{self.room}, {self.person}"
