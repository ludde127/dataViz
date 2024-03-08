from django import template
from wagtail.models import Page, Site

from study_notes.models import NoteTagIndexPage

register = template.Library()


@register.simple_tag(takes_context=True, name="get_site_root")
def get_site_root(context):
    # This returns a core.Page. The main menu needs to have the site.root_page
    # defined else will return an object attribute error ('str' object has no
    # attribute 'get_children')
    root = Site.find_for_request(context['request']).root_page
    tree = collect(root)
    return tree


def collect(node: Page):
    return {
        "page": node,
        "children": [collect(child) for child in node.get_children() if
                     not isinstance(child.specific, NoteTagIndexPage)]
    }
