from django.urls import path
from . import views


urlpatterns = [
        path("", views.index, name="booking_index"),
        path("<str:booking_uuid>/", views.booking, name="Booking"),
        path("<str:booking_uuid>/add-selected/", views.add_selected_time_slot, name="add_selected_timeslot"),
]