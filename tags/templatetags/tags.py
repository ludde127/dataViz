import datetime

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


@register.simple_tag
def path_to_breadcrumb_list(path: str):
    return [p.capitalize() for p in path.split("/")[1:]]


@register.filter
def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


@register.simple_tag(takes_context=True)
def file_version_hash(context):
    version = f"?v={context['GIT_HASH']}"
    if context['DEBUG']:
        version += f"-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    return version
