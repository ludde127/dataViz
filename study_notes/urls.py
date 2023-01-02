from django.urls import path
from . import views

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter

api_router = WagtailAPIRouter("wagtail-api")
api_router.register_endpoint('pages', PagesAPIViewSet)

urlpatterns = [
        path("auto/", api_router.urls, name="wagtail_api"),
        path("change/subscribe/", views.subscribe_to_flashcard_group),
        path("change/unsubscribe/", views.unsubscribe_to_flashcard_group),
        path("change/flashcard-interaction/", views.add_flashcard_interactions),
        path("users/<str:user>", views.user_profile, name="user_profile")
    ]