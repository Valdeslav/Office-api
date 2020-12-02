from django.contrib import admin

from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['room', 'start_date', 'end_date', 'person']
admin.site.register(Reservation, ReservationAdmin)
