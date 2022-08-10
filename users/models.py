from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.db.models import Q


class User(AbstractUser):
    """Here for the future as a
    switch is annoying."""
    pass


class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField("Profile picture", width_field=128, height_field=128,
                                      null=True, default=None, blank=True)
    description = models.TextField("Description about me.", max_length=1000)
    api_access_count = models.IntegerField("Amount of calls to the api", default=0)

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


class ContentPermissions(models.Model):
    view_permission = models.ManyToManyField(NormalUser, "view_permission")
    change_permission = models.ManyToManyField(NormalUser, "change_permission")
    delete_permission = models.ManyToManyField(NormalUser, "delete_permission")
    add_permission = models.ManyToManyField(NormalUser, "add_permission")
    all_can_view = models.BooleanField(default=True)

    def get_change_permission(self, request):
        return self.change_permission.contains(request.user.normaluser)

    def get_delete_permission(self, request):
        return self.delete_permission.contains(request.user.normaluser)

    def get_add_permission(self, request):
        return self.add_permission.contains(request.user.normaluser)

    def get_view_permission(self, request):
        return self.view_permission.contains(request.user.normaluser)

    def for_normaluser(self):
        return hasattr(self, "normaluser")

    def for_baseblock(self):
        return hasattr(self, "baseblock")

    def for_content(self):
        return hasattr(self, "content")

    def __str__(self):
        if self.for_normaluser():
            return f"Permissions for user {self.normaluser.user.username}'s profile."
        elif self.baseblock:
            return f"Permissions for block {self.baseblock.id}."
        elif self.content:
            return f"Permissions for content {self.content.id} by {self.content.author}"
        else:
            raise NotImplementedError("This usage of the class is not already implemented.")


class Permissions(models.Model):
    public = models.BooleanField("Is public", default=False)
    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name="+")
    subjects = models.ManyToManyField(NormalUser, verbose_name="Users affected by white/black-list", related_name="+")

    is_whitelist = models.BooleanField("Is whitelist", default=True)
    is_blacklist = models.BooleanField("Is blacklist", default=False)

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

        return _class.objects.filter(Q(owner=user) | ((Q(public=True) &
                                                          (~Q(subjects__in=(user,)))) |
                                                         (Q(public=False) & Q(
                                                             subjects__in=(user,)))))
