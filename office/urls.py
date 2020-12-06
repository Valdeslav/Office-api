from django.urls import re_path

from .views import RoomView, FreeRoomView, ReservInfoView

app_name = "office"

urlpatterns = [
    # get room by id update
    re_path(r'^rooms/<int:number>$', RoomView.as_view()),
    # get all rooms or create  room
    re_path(r'^rooms/$', RoomView.as_view()),
    # get free rooms on the specified date
    re_path(r'^rooms/free/<req_date>$', FreeRoomView.as_view()),
    # get information about which people reserved room on the specified date
    re_path('^rooms/reserv-info/<int:number>/<req_date>$', ReservInfoView.as_view()),
    # get information about which people reserved room during the entire time
    re_path('^rooms/reserv-info/<int:number>$', ReservInfoView.as_view()),
]


