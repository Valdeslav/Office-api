from django.db import models
from django.core.validators import MaxValueValidator


class Room(models.Model):
    number = models.PositiveIntegerField(db_index=True)
    seats_num = models.PositiveIntegerField(
        validators=[MaxValueValidator(30, message="Number of seats must be lower than 30"), ])

    class Meta:
        ordering = ('number',)

    def __str__(self):
        return f"room {self.number}"
