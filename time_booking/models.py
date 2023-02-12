import uuid as uuid
from django.db import models
from django.urls import reverse

from users.models import NormalUser


# Create your models here.
class TimeSlotBooking(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)

    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name="+")
    uuid = models.UUIDField("uuid", default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        unique_together = ["owner", "name"]

    def url(self):
        return reverse("Booking", kwargs={"booking_uuid": self.uuid})



class TimeSlot(models.Model):
    time_slot_start = models.DateTimeField("Start date")
    time_slot_end = models.DateTimeField("End date")

    added_by = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name="+")

    master = models.ForeignKey(to=TimeSlotBooking, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["master", "time_slot_start", "time_slot_end"]

    def add_accepted_by(self, user: NormalUser, anon_string=""):
        print("r12")
        if user.user.is_anonymous and anon_string:
            AcceptedTimeSlot.objects.create(accepted_by_name=anon_string, time_slot=self).save()
        elif user.user.is_authenticated:
            AcceptedTimeSlot.objects.create(accepted_by=user, accepted_by_name="USER:"+str(user.id), time_slot=self).save()
        else:
            return ValueError("User is not logged in and the anon_string was empty.")

    def add_accepted_by_anon(self, anon_string=""):
        if anon_string:
            AcceptedTimeSlot.objects.create(accepted_by_name=anon_string, time_slot=self).save()
        else:
            return ValueError("User is not logged in and the anon_string was empty.")

class AcceptedTimeSlot(models.Model):
    accepted_by = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name="+", blank=True, null=True)

    accepted_by_name = models.CharField(max_length=100, blank=True, verbose_name="Fill if not logged in.")

    time_slot = models.ForeignKey(to=TimeSlot, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["accepted_by_name", "time_slot"]