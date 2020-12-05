from django.urls import path

from .views import RoomView, FreeRoomView, ReservInfoView

app_name = "office"

urlpatterns = [
    # get room by id
    path('rooms/<int:number>/', RoomView.as_view()),
    # get all rooms or create (update) room
    path('rooms/', RoomView.as_view()),
    # get free rooms on the specified date
    path('rooms/free/<req_date>/', FreeRoomView.as_view()),
    # get information about which people reserved room on the specified date
    path('rooms/reserv-info/<int:number>/<req_date>/', ReservInfoView.as_view()),
    # get information about which people reserved room during the entire time
    path('rooms/reserv-info/<int:number>/', ReservInfoView.as_view()),
]


