from dataViz.admin import admin_site
from .models import BaseBlock
from reversion.admin import VersionAdmin


# Register your models here.

class RevisableBlock(VersionAdmin):
    pass


admin_site.register(BaseBlock, RevisableBlock)