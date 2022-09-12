import datetime
import time
from pprint import pprint

import pandas as pd
from django.db import models
from users.models import NormalUser
from energy_utils.tesla.client import Client
# Create your models here.


def scheduled_charging():
    latest = sorted([v for v in Charging.objects.filter(valid=True).all() if v.still_valid()],
                    key=lambda _: _.mean_price)  # Cheapest to most expensive.
    if len(latest) == 0:
        return None
    return latest[0]


class EnergyUsage(models.Model):
    amount = \
        models.FloatField(verbose_name="Usage in kWh", default=0)
    time = models.DateTimeField(verbose_name="Time", auto_created=True)
    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE)


class TeslaChargingAction(models.Model):
    start_stop = models.BooleanField("If this was start command this is True if stop it is False")
    time = models.DateTimeField(verbose_name="Time", auto_created=True, auto_now=True)

    current_pct_charged = models.FloatField()

    def __str__(self):
        return f"{self.time}"


class TeslaVehicle(models.Model):
    vehicle_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=300)

    is_charging = models.BooleanField(default=False)
    actions = models.ManyToManyField(TeslaChargingAction)


class TeslaTokens(models.Model):
    token = models.CharField(verbose_name="Token", max_length=1000, editable=False, default=None, null=True)
    expiry = models.DateTimeField("Token expiry", editable=True, default=None, null=True)
    refresh_token = models.CharField("Refresh token", max_length=1000, editable=False, default=None, null=True)

    verifier = models.CharField("Verifier", max_length=200, editable=False, default=None, null=True)
    smart_charging = models.BooleanField("Enable smart charging", default=False)
    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    should_be_charging_now = models.BooleanField(default=False)

    vehicles = models.ManyToManyField(TeslaVehicle)

    energy_zone = models.CharField("Energy zone", max_length=15, default="SE_4")

    def get_url_for_token_creation(self):
        url, verf = Client.create_auth_url()
        self.verifier = verf
        self.save()
        return url

    def create_tokens(self, url):
        self.token, self.refresh_token, expiry =\
            Client.get_auth_token_from_url(url, self.verifier)
        self.expiry = datetime.datetime.fromtimestamp(expiry, tz=None)
        self.save()

    def refresh_tokens(self):
        self.token, self.refresh_token, expiry =\
            self.__new_client().refresh_token()
        self.expiry = datetime.datetime.fromtimestamp(expiry, tz=None)

        self.save()

    def __new_client(self):
        return Client(self.token, self.refresh_token,
                      self.expiry.timestamp(), (v.vehicle_id for v in self.vehicles.all()))

    def all_vehicles(self, client=None, force_vehicle_check=False):
        if client is None:
            try:
                client = self.__new_client()
            except Exception as e:
                if force_vehicle_check:
                    raise e
        ids = {int(v.vehicle_id) for v in self.vehicles.all()}
        if force_vehicle_check:
            for vehicle_id, display_name in client.query_vehicles().items():
                if vehicle_id not in ids:
                    self.vehicles.add(TeslaVehicle.objects.create(vehicle_id=vehicle_id, display_name=display_name))
                    ids.add(vehicle_id)
        for id in ids:
            client.wake_up(id) # Wakes them so they are ready to take commands.

        return ids

    def __charging_action(self, vehicle_id, started_charging, save=True, client=None):
        """Set started_charging to true if this is to save the action of starting a charge."""
        if client is None:
            client = self.__new_client()
        current_pct_charged = float(client.charge_state(vehicle_id)["response"]["battery_level"])
        vehicle = self.vehicles.get(vehicle_id=vehicle_id)
        action = vehicle.actions
        action.add(
            TeslaChargingAction.objects.create(start_stop=started_charging, current_pct_charged=current_pct_charged))
        if save:
            self.save()

    def stop_charging_all(self, force=True):
        if self.should_be_charging_now or force:
            client = self.__new_client()
            for v in self.all_vehicles(client):
                client.stop_charging(v)
                self.__charging_action(v, started_charging=False, save=False, client=client)
            self.should_be_charging_now = False
            self.save()

    def start_charging_all(self):
        client = self.__new_client()
        for v in self.all_vehicles(client):
            client.start_charging(v)
            self.__charging_action(v, started_charging=True, save=False, client=client)
        self.should_be_charging_now = True
        self.save()

    def is_charging(self):
        client = self.__new_client()
        states = [client.charge_state(v) for v in self.all_vehicles(client)]
        return any((state["response"]["charging_state"] == "Charging" for state in states))

    def seconds_until_expiry(self):
        return self.expiry.timestamp() - datetime.datetime.now().timestamp()

    def has_expired(self):
        if self.expiry:
            return self.seconds_until_expiry() < 0
        return True

    def __str__(self):
        return f"TOKEN -- {self.owner}"


class Charging(models.Model):
    start_time = models.DateTimeField(default=None, null=True)
    end_time = models.DateTimeField(default=None, null=True)

    mean_price = models.FloatField(default=0)
    valid = models.BooleanField(default=True)

    class Meta:
        unique_together = ["start_time", "end_time"]  # Easier to extend later.

    def __str__(self):
        return f"{self.start_time} Until {self.end_time}; {self.mean_price}"

    def should_charge(self):
        return self.start_time.timestamp() <= time.time() <= self.end_time.timestamp()

    def still_valid(self):
        self.valid = time.time() <= self.end_time.timestamp()
        self.save()
        return self.valid


class EnergyDayAhead(models.Model):
    price = models.FloatField(blank=False)
    time = models.DateTimeField(blank=False)
    energy_zone = models.CharField(blank=False, max_length=10)

    class Meta:
        unique_together = ["time", "energy_zone"]


