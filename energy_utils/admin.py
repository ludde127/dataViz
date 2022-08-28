from dataViz.admin import admin_site
from .models import TeslaTokens, TeslaChargingAction, Charging
# Register your models here.

admin_site.register(TeslaTokens)
admin_site.register(TeslaChargingAction)
admin_site.register(Charging)
