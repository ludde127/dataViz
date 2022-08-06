import uuid

from django.db import models
from content.models import Content, BaseTextMediaContent
from users.models import NormalUser, ContentPermissions
# Create your models here.


class BaseBlock(BaseTextMediaContent):
    permissions = models.OneToOneField(verbose_name="permissions", to=ContentPermissions,
                                       on_delete=models.CASCADE, null=True, blank=True)
    content = models.ManyToManyField(Content, "content")
    human_identifiable_id = models.CharField(max_length=100, default=uuid.uuid4, null=False, unique=True)
    video = None  # Disallow videos

    @staticmethod
    def get_viewable(request):
        """Gets the content that the given user has access to. If none a empty list is returned."""

        user = request.user
        try:
            if user.is_anonymous or not user.normaluser:
                return BaseBlock.objects.filter(permissions__all_can_view=True)
            return BaseBlock.objects.filter(permissions__view_permission__in=(user.normaluser, ))
        except BaseBlock.DoesNotExist:
            return []


