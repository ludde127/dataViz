from django.urls import path
from . import views

urlpatterns = [
    path("", views.text_sections, name="text_sections_api"),
    path("/pages/", views.pages, name="pages_api")
]