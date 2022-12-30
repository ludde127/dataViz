from django.urls import path
from . import views

urlpatterns = [
        path("get-flashcards/<str:notepage_id>", views.get_flashcards, name="get_flashcards")
    ]