from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("plot/<str:key>", views.plot, name="plot")
]