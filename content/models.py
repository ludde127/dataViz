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


class ContentEdits(BaseTextContent):
    title = models.CharField(max_length=80, null=False)
    text = models.TextField(max_length=10000, null=False)
    created = models.DateTimeField("Created", auto_now_add=True)

    # Single linked list of edits.
    next_edit = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Edit {self.created} by {self.owner.user.username}"

    def last_edit(self):
        # Right now this is slow, should not matter in normal use.
        last = None
        while n := self.next_edit:
            last = n
        return last


class Content(BaseTextMediaContent):
    edits = models.OneToOneField(ContentEdits, on_delete=models.CASCADE, null=True, editable=False)
    comments = models.ManyToManyField("self", verbose_name="Comments", null=True, blank=True, default=None)

    def is_long(self):
        return len(self.text) > 300

    def is_short(self):
        return not self.is_long()

    def edited(self):
        return self.edits is not None

    def __comments(self):
        return self.comments.exclude(id__lte=self.id)

    def has_comments(self):
        return self.comments is not None and self.__comments().exists()

    def get_comments(self, user):
        comments = self.comments.exclude(id__lte=self.id).filter(Permissions.can_user_view_query(user.normaluser))
        return comments

    def safe_delete(self):
        edit = ContentEdits(title=self.title, text=self.text, owner=self.owner)
        self.insert_edit(edit)
        self.title = "REMOVED"
        self.text = "REMOVED"
        self.is_removed = True
        self.edits.save()
        self.save()

    def insert_edit(self, edit):
        """Inserts the edit into the potentially empty singlelinked chain."""
        if self.edits:
            self.edits.last_edit().next_edit = edit
            self.edits.last_edit().save()
        else:
            self.edits = edit