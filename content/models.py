from django.db import models
from users.models import Permissions, NormalUser


# Create your models here.


class BaseTextContent(Permissions):
    title = models.CharField(max_length=80, null=False)
    text = models.TextField(max_length=10000, null=False)
    created = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Content: {self.title}"


class BaseTextMediaContent(BaseTextContent):
    image = models.ImageField("Image", upload_to="content/images/", null=True, blank=True)
    video = models.FileField("Video", upload_to="content/video/", null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Media-Content: {self.title} "


class AbstractContent(BaseTextMediaContent):
    comments = models.ManyToManyField("self", verbose_name="Comments", null=True, blank=True, default=None)

    def is_long(self):
        return len(self.text) > 300

    def is_short(self):
        return not self.is_long()

    def __comments(self):
        return self.comments.exclude(id__lte=self.id)

    def has_comments(self):
        return self.comments is not None and self.__comments().exists()

    def get_comments(self, user):
        comments = self.comments.exclude(id__lte=self.id).filter(Permissions.can_user_view_query(user.normaluser))
        return comments

    def safe_delete(self):
        self.title = "REMOVED"
        self.text = "REMOVED"
        self.is_removed = True
        self.save()

    class Meta:
        abstract = True


class Content(AbstractContent):
    pass
