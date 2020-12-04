from django.urls import path

from .views import RoomView, FreeRoomView, ReservInfoView

app_name = "office"

urlpatterns = [
    path('rooms/<int:number>', RoomView.as_view()),
    path('rooms/', RoomView.as_view()),
    path('rooms/free/<req_date>', FreeRoomView.as_view()),
    path('rooms/reserv-info/<int:number>/<req_date>', ReservInfoView.as_view()),
]


