from django.urls import path
from .views import ReservationView

app_name = "reservation"

urlpatterns = [
    # get reservation by id or update reservation
    path('reservations/<int:res_id>', ReservationView.as_view()),
    # get all reservations or create
    path('reservations/', ReservationView.as_view()),
]
