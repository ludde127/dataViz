from dataViz.admin import admin_site
from .models import TextSection, Page

# Register your models here.
admin_site.register(TextSection)
admin_site.register(Page)