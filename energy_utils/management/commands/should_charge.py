import time

from django.core.management.base import BaseCommand, CommandError
from energy_utils.models import TeslaTokens
from energy_utils.electricity_prices.get_data import Prices
import datetime


class Command(BaseCommand):
    help = 'Checks if charging should be started.'

    def handle(self, *args, **options):
        WINDOW_SIZE = 3
        p = Prices()
        cheapest = p.sorted_rolling(WINDOW_SIZE, "SE_4")["prices"]
        end_of_cheap = list(cheapest.index)[0].timestamp()
        start_charging = end_of_cheap - WINDOW_SIZE * 3600
        all_ = TeslaTokens.objects.filter(smart_charging=True).all()

        if start_charging <= time.time() <= end_of_cheap:
            e = 0
            n = 0
            for tokens in all_:
                try:
                    tokens.start_charging_all()
                    n += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))
                    e += 1
            self.stdout.write(self.style.SUCCESS(f"Ran the charging script, started charging for"
                                                 f" {n}/{len(all_)} with {e} errors."))
        else:
            for tokens in all_:
                tokens.stop_charging_all()
            self.stdout.write(self.style.SUCCESS(f"Will not start charging"
                                                 f" before {datetime.datetime.fromtimestamp(start_charging)}"))