from django.urls import path
from . import views

urlpatterns = [
    path("access/<str:key>", views.access_data, name="access_data")
]