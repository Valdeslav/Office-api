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

    # check if seats are available
    def check_seats(self):
        taken_seats = Reservation.objects.filter(
            id__lt=self.id,
            id__gt=self.id,
            room=self.room,
            start_date__lte=self.end_date,
            end_date__gte=self.start_date
        ).count()

        return self.room.seats_num <= taken_seats

    # check if exist reservations in the specified interval,
    # save and create response data
    def save_reserv(self, method):
        if self.check_seats():
            return {"error": "all seats are reserved"}

        reservations = Reservation.objects.filter(person=self.person)
        for reservation in reservations:
            if self.check_dates(reservation.start_date, reservation.end_date) and\
               self.id != reservation.id:
                return {
                    'error': f"person {self.person} has reserved room in date "
                             f"interval {self.start_date} - {self.end_date}"
                }

        self.save()
        return {
            'success': f"Reservation '{self}' {method} successfully"
        }

    # check if intervals intersect
    def check_dates(self, start_date, end_date):
        latest_start = max(start_date, self.start_date)
        earliest_end = min(end_date, self.end_date)
        return latest_start <= earliest_end

    def __str__(self):
        return f"{self.room}, {self.person}"
