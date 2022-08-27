from django.urls import path
from . import views

urlpatterns = [
        path("", views.energy_index, name="energy_index"),
        path("charging/start", views.start_charging, name="vehicle_start_charging"),
        path("charging/stop", views.stop_charging, name="vehicle_stop_charging")
    ]