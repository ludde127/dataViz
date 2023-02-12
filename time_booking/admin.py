from dataViz.admin import admin_site
from .models import *
# Register your models here.
admin_site.register(TimeSlotBooking)
admin_site.register(TimeSlot)
admin_site.register(AcceptedTimeSlot)