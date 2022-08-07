from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="social_index"),
    path("block/<str:hid>", views.block, name="block"),
    path("content/<int:id>", views.content, name="content")
]