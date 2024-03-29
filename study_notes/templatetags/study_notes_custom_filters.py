from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_sorted_live_children(page):
    return sorted([c for c in page.get_children() if c.live], key=lambda p: p.title)
