from django.contrib import admin
# Register your models here.


class AdminSite(admin.AdminSite):
    pass


admin_site = AdminSite(name="admin_site")