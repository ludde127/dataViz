import time

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from energy_utils.models import Charging
from energy_utils.electricity_prices.get_data import Prices
import datetime


class Command(BaseCommand):
    help = 'Checks if charging should be started.'

    def handle(self, *args, **options):
        WINDOW_SIZE = 3
        p = Prices()
        cheapest = pd.DataFrame(p.sorted_rolling(WINDOW_SIZE, "SE_4")["prices"][[0]]).reset_index()
        #print(cheapest)
        #print(type(cheapest["index"]), type(cheapest["prices"]))
        end_of_cheap = cheapest["index"][0].timestamp()
        start_charging = end_of_cheap - WINDOW_SIZE * 3600

        Charging.objects.update_or_create(start_time=datetime.datetime.fromtimestamp(start_charging),
                                          end_time=datetime.datetime.fromtimestamp(end_of_cheap),
                                          mean_price=cheapest["prices"][0])
        self.stdout.write(self.style.SUCCESS(f"Will start charging {datetime.datetime.fromtimestamp(start_charging)}"))