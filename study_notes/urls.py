from django.urls import path
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet

from . import views

api_router = WagtailAPIRouter("wagtail-api")
api_router.register_endpoint('pages', PagesAPIViewSet)

urlpatterns = [
    path("auto/", api_router.urls, name="wagtail_api"),
    path("change/subscribe/", views.subscribe_to_flashcard_group),
    path("change/unsubscribe/", views.unsubscribe_to_flashcard_group),
    path("change/flashcard-interaction/", views.add_flashcard_interactions),
]
