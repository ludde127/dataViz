from dataViz.admin import admin_site
from .models import *
from reversion.admin import VersionAdmin

# Register your models here.


class ReversionContent(VersionAdmin):
    pass


admin_site.register(Content, ReversionContent)
