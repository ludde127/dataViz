# Create your models here.
from django.db import models
from dataViz.settings import BASE_CONTEXT
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context.update(BASE_CONTEXT)
        return context

class UserPage(Page):
    intro = models.CharField(blank=True, max_length=250)
    body = RichTextField(blank=True)

    subpage_types = []
    parent_page_type = ["wagtail_home.UsersPage"]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context.update(BASE_CONTEXT)
        return context

class UsersPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    subpage_types = ["wagtail_home.UserPage"]
    parent_page_type = ["wagtail_home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context.update(BASE_CONTEXT)
        return context