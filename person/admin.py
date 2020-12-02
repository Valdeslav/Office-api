from django.contrib import admin

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', ]
admin.site.register(Person, PersonAdmin)

