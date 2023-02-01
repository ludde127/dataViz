from .views import index, stock_api
# Create your views here.

from django.urls import path
urlpatterns = [
    path("", index, name="stock_index"),
    path("register", stock_api, name="stock_register")
]
