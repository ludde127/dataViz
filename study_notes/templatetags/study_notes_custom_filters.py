from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """print("---")
    print(dictionary)
    print(key)
    print("...")"""
    return dictionary.get(key)


@register.filter
def get_live_children(page):
    return [c for c in page.get_children() if c.live]
