import uuid

from django.core.exceptions import ValidationError
from django.db import models
from content.models import Content, BaseTextMediaContent
from users.models import NormalUser
# Create your models here.


class BaseBlock(BaseTextMediaContent):
    content = models.ManyToManyField(Content, "content")
    human_identifiable_id = models.CharField(verbose_name="Display name (no spaces)", max_length=100,
                                             default="", null=False, unique=True)
    video = None  # Disallow videos

    def clean(self):
        if " " in self.human_identifiable_id:
            raise ValidationError("The Display name may not contain spaces.")
        return super().clean()

    def safe_delete(self):
        self.title = "REMOVED"
        self.text = "REMOVED"
        self.image = None
        self.video = None
        self.is_removed = True
        self.save()

    @property
    def hid(self):
        return self.human_identifiable_id


