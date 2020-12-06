from django.urls import path

from .views import PersonView, ReservInformationView

app_name = "person"

urlpatterns = [
    # get person by id or update
    path('persons/<int:id>', PersonView.as_view()),
    # get all persons or create person
    path('persons', PersonView.as_view()),
    # get all reserved rooms of person
    path('persons/<int:pers_id>/res-rooms', ReservInformationView.as_view()),
    # get reserved room on the specified date
    path('persons/<int:pers_id>/res-rooms/<req_date>', ReservInformationView.as_view()),
]
