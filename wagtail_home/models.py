# Create your models here.

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from dataViz.settings import BASE_CONTEXT


def filter_non_viewable(user, qs):
    """Given a user and a queryset this filters all the objects not viewable by the user. If page_model_string is supplied
    only matching models are given (I THINK)"""
    pages = qs.live()

    # Unauthenticated users can only see public pages
    if not user.is_authenticated:
        pages = pages.public()
    # Superusers can implicitly view all pages. No further filtering required
    elif not user.is_superuser:
        # Get all page ids where the user's groups do NOT have access to
        """disallowed_ids = PageViewRestriction.objects.exclude(groups__id=user.groups.all()).values_list(
            "page",
            flat=True)
        # Exclude all pages with disallowed ids
        pages = pages.exclude(id__in=disallowed_ids)
        print("PAGES", pages)"""
        # TODO implement an actual way to limit this
    return pages


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context.update(BASE_CONTEXT)
        context["children"] = filter_non_viewable(request.user, self.get_children())
        context["title"] = "Pages"

        return context
