from users.models import NormalUser, Permissions
from . import register


@register.simple_tag
def all_viewable(_class, user: NormalUser):
    return Permissions.all_user_can_view(user, _class)


@register.simple_tag
def all_viewable_comments(content, user: NormalUser):
    return content.get_comments(user)


@register.filter
def get_comments(content, user: NormalUser):
    return all_viewable_comments(content, user)


@register.filter
def bool_to_int(boolean):
    return 1 if boolean else 0