import uuid

from django.db import models
from content.models import Content, BaseTextMediaContent
from users.models import NormalUser
# Create your models here.


class BaseBlock(BaseTextMediaContent):
    content = models.ManyToManyField(Content, "content")
    human_identifiable_id = models.CharField(max_length=100, default=uuid.uuid4, null=False, unique=True)
    video = None  # Disallow videos



