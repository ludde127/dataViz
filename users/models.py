from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    """Here for the future as a
    switch is annoying."""
    pass


class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField("Profile picture", width_field=128, height_field=128,
                                      null=True, default=None, blank=True)
    description = models.TextField("Description about me.", max_length=1000)
    permissions = models.OneToOneField(verbose_name="permissions", to="users.ContentPermissions",
                                       on_delete=models.CASCADE, null=True, editable=False, default=None)
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