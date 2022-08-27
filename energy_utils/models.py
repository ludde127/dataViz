import datetime
from pprint import pprint

import pandas as pd
from django.db import models
from users.models import NormalUser
from energy_utils.tesla.client import Client
# Create your models here.


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
    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE)

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
        return Client(self.token, self.refresh_token, self.expiry.timestamp())

    def all_vehicles(self, client=None):
        if client is not None:
            return client.vehicles
        return self.__new_client().vehicles

    def stop_charging_all(self):
        client = self.__new_client()
        for v in self.all_vehicles(client).keys():
            client.stop_charging(v)
        TeslaChargingAction.objects.create(start_stop=False, token=self)

    def start_charging_all(self):
        client = self.__new_client()
        for v in self.all_vehicles(client).keys():
            client.start_charging(v)
        TeslaChargingAction.objects.create(start_stop=True, token=self)

    def is_charging(self):
        client = self.__new_client()
        states = [client.charge_state(v) for v in client.vehicles]
        return any((state["response"]["charging_state"] == "Charging" for state in states))


class TeslaChargingAction(models.Model):
    start_stop = models.BooleanField("If this was start command this is True if stop it is False")
    time = models.DateTimeField(verbose_name="Time", auto_created=True, auto_now=True)

    token = models.ForeignKey(TeslaTokens, on_delete=models.CASCADE)
