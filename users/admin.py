from django.contrib.auth.models import Group
from dataViz.admin import admin_site
from .models import User, NormalUser, ContentPermissions
from django.contrib.auth.admin import UserAdmin, GroupAdmin
# Register your models here.

admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
admin_site.register(NormalUser)
admin_site.register(ContentPermissions)