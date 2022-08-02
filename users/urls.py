from django.urls import path
from . import views
urlpatterns = [
    path("login", views.login_view, name="login"),
    path("create-account", views.create_account, name="create_account"),
    path("reset-password", views.reset_password, name="reset_password"),
    path("logout", views.logout_view, name="logout")
]
