from django import template

register = template.Library()
@register.filter
def get_item(dictionary, key):
    """print("---")
    print(dictionary)
    print(key)
    print("...")"""
    return dictionary.get(key)