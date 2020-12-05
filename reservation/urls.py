from django.urls import path
from .views import ReservationView

app_name = "reservation"

urlpatterns = [
    # get reservation by id or create (update) reservation
    path('reservations/<int:id>/', ReservationView.as_view()),
    # get all reservations
    path('reservations/', ReservationView.as_view()),
]
