from dataViz.admin import admin_site
from .models import TeslaTokens, TeslaChargingAction, Charging, EnergyDayAhead, TeslaVehicle
# Register your models here.

admin_site.register(TeslaTokens)
admin_site.register(TeslaChargingAction)
admin_site.register(Charging)
admin_site.register(EnergyDayAhead)
admin_site.register(TeslaVehicle)