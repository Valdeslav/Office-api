from django.contrib import admin

from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'seats_num']
admin.site.register(Room, RoomAdmin)
