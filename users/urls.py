from django.urls import path
from . import views
import study_notes.views as s_views
urlpatterns = [
    path("login", views.login_view, name="login"),
    path("create-account", views.create_account, name="create_account"),
    path("reset-password", views.reset_password, name="reset_password"),
    path("logout", views.logout_view, name="logout"),
    path("u/<str:user>", s_views.user_profile, name="user_profile"),
    path("me/flashcards", s_views.view_flashcards_info, name="view_flashcard_stats")
]
