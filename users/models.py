from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db.models import Q
from wagtail.snippets.models import register_snippet


class User(AbstractUser):
    """Here for the future as a
    switch is annoying."""
    pass

@register_snippet
class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    profile_image = models.ImageField("Profile picture",
                                      null=True, default=None, blank=True)
    description = models.TextField("Description about me.", max_length=1000)
    api_access_count = models.IntegerField("Amount of calls to the api", default=0, editable=False)

    def __str__(self):
        return self.user.__str__()

    def has_change_permission(self, content):
        return self in content.permissions.change_permission

    def has_view_permission(self, content):
        return self in content.permissions.view_permission

    def has_add_permission(self, content):
        return self in content.permissions.add_permission

    def has_delete_permission(self, content):
        return self in content.permissions.delete_permission


class Permissions(models.Model):
    public = models.BooleanField("Is public", default=False)
    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name="+")
    subjects = models.ManyToManyField(NormalUser, verbose_name="Users affected by white/black-list", related_name="+")

    is_whitelist = models.BooleanField("Is whitelist", default=True)
    is_blacklist = models.BooleanField("Is blacklist", default=False)
    is_removed = models.BooleanField("Is this object removed", default=False)

    class Meta:
        abstract = True

    def clean(self):
        if self.is_whitelist and self.is_blacklist:
            raise ValidationError("The permission may either be in whitelist or blacklist mode, not both.")
        if self.public and self.is_whitelist:
            raise ValidationError("Only blacklist mode is available when public.")
        if self.is_blacklist and not self.public:
            raise ValidationError("Only whitelist mode is available when not public.")
        return super().clean()

    @staticmethod
    def can_user_view_query(user):
        return Q(owner=user) | ((Q(public=True) &
                                 (~Q(subjects__in=(user,)))) |
                                (Q(public=False) & Q(
                                    subjects__in=(user,))))

    @staticmethod
    def all_user_can_view(user: NormalUser, _class):
        """query = Q(owner=user)

        public_not_blacklisted = Q(permissions__public=True)

        # Blacklist mode is always on when its public.
        public_not_blacklisted.add(Q(permissions__subjects__in=(user,)).negate(), Q.AND)

        not_public_whitelist = Q(permissions__public=False)
        not_public_whitelist.add(Q(permissions__is_whitelist=True), Q.AND)
        not_public_whitelist.add(Q(permissions__subjects__in=(user,)), Q.AND)
        query.add(public_not_blacklisted, Q.OR)
        query.add(not_public_whitelist, Q.OR)"""

        return _class.objects.filter(Permissions.can_user_view_query(user))
