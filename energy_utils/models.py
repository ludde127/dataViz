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
                    key=lambda _: _.mean_price) # Cheapest to most expensive.
    if len(latest) == 0:
        return None
    return latest[0]


class EnergyUsage(models.Model):
    amount = \
        models.FloatField(verbose_name="Usage in kWh", default=0)
    time = models.DateTimeField(verbose_name="Time", auto_created=True)
    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE)



class TeslaTokens(models.Model):
    token = models.CharField(verbose_name="Token", max_length=1000, editable=False, default=None, null=True)
    expiry = models.DateTimeField("Token expiry", editable=True, default=None, null=True)
    refresh_token = models.CharField("Refresh token", max_length=1000, editable=False, default=None, null=True)

    verifier = models.CharField("Verifier", max_length=200, editable=False, default=None, null=True)
    smart_charging = models.BooleanField("Enable smart charging", default=False)
    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    should_be_charging_now = models.BooleanField(default=False)

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
        try:
            return Client(self.token, self.refresh_token, self.expiry.timestamp())
        except AssertionError:
            return None

    def all_vehicles(self, client=None):
        if client is not None:
            return client.vehicles
        return self.__new_client().vehicles

    def stop_charging_all(self, force=True):
        if self.should_be_charging_now or force:
            client = self.__new_client()
            for v in self.all_vehicles(client).keys():
                client.stop_charging(v)
            self.should_be_charging_now = False

            TeslaChargingAction.objects.create(start_stop=False, token=self)
            self.save()

    def start_charging_all(self):
        client = self.__new_client()
        for v in self.all_vehicles(client).keys():
            client.start_charging(v)
        self.should_be_charging_now = True

        TeslaChargingAction.objects.create(start_stop=True, token=self)
        self.save()

    def is_charging(self):
        client = self.__new_client()
        states = [client.charge_state(v) for v in client.vehicles]
        return any((state["response"]["charging_state"] == "Charging" for state in states))

    def seconds_until_expiry(self):
        return self.expiry.timestamp() - datetime.datetime.now().timestamp()

    def has_expired(self):
        if self.expiry:
            return self.seconds_until_expiry() < 0
        return True

    def __str__(self):
        return f"TOKEN -- {self.token.owner.user.username}"


class TeslaChargingAction(models.Model):
    start_stop = models.BooleanField("If this was start command this is True if stop it is False")
    time = models.DateTimeField(verbose_name="Time", auto_created=True, auto_now=True)

    token = models.ForeignKey(TeslaTokens, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.time}, -- {self.token.owner.user.username}"


class Charging(models.Model):
    start_time = models.DateTimeField(default=None, null=True)
    end_time = models.DateTimeField(default=None, null=True)

    mean_price = models.FloatField(default=0)
    valid = models.BooleanField(default=True)

    class Meta:
        unique_together = ["start_time", "end_time"]  # Easier to extend later.

    def should_charge(self):
        return self.start_time.timestamp() <= time.time() <= self.end_time.timestamp()

    def still_valid(self):
        self.valid = time.time() <= self.end_time.timestamp()
        self.save()
        return self.valid



