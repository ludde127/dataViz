from . import register


@register.simple_tag
def can_view(request, content):
    return content.permissions.get_view_permission(request)


@register.simple_tag
def can_change(request, content):
    return content.permissions.get_change_permission(request)


@register.simple_tag
def can_delete(request, content):
    return content.permissions.get_delete_permission(request)


@register.simple_tag
def can_add(request, content):
    return content.permissions.get_add_permission(request)


@register.simple_tag
def get_comments_with_permissions(request, content):
    comments = content.get_comments()
    return [CommentWithPermissions(c, c.permissions_as_dict(request)) for c in comments]


class CommentWithPermissions:
    def __init__(self, comment, permission):
        self.__comment = comment
        self.__permission = permission
    
    def __getattr__(self, item):
        if hasattr(self.__comment, item):
            return self.__comment.item
        elif item == "can_view":
            return self.__permission["can_view"]
        elif item == "can_change":
            return self.__permission["can_change"]
        elif item == "can_delete":
            return self.__permission["can_delete"]
        elif item == "can_add":
            return self.__permission["can_add"]
        else:
            raise AttributeError(str(item) + " Does not exist")