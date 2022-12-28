# Create your models here.
from django.db import models
from wagtail.models import PageViewRestriction

from dataViz.settings import BASE_CONTEXT
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

def filter_non_viewable(user, qs, page_model_string):
    pages = qs.live()

    # Unauthenticated users can only see public pages
    if not user.is_authenticated:
        pages = pages.public()
    # Superusers can implicitly view all pages. No further filtering required
    elif not user.is_superuser:
        # Get all page ids where the user's groups do NOT have access to
        disallowed_ids = PageViewRestriction.objects.exclude(groups__id=user.groups.all()).values_list(
            page_model_string,
            flat=True)
        # Exclude all pages with disallowed ids
        pages = pages.exclude(id__in=disallowed_ids)
    return pages

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