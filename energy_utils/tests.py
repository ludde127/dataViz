from django.test import TestCase

from energy_utils.models import TeslaTokens


class EnergyUtils(TestCase):
    def test_refreshes(self):
        for t in TeslaTokens.objects.all():
            t.refresh_tokens()

    def test_is_charging(self):
        charging_num = 0
        for t in TeslaTokens.objects.all():
            if t.is_charging():
                charging_num += 1
        print(f"Number charging is {charging_num}")