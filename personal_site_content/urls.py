from django.urls import path
from . import views

urlpatterns = [
    path("api/", views.text_sections, name="text_sections_api")
]