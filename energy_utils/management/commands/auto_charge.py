import time

import pytz
from django.core.management.base import BaseCommand, CommandError
from energy_utils.models import TeslaTokens, Charging
import datetime


class Command(BaseCommand):
    help = 'Checks if charging should be started.'

    def handle(self, *args, **options):
        latest = sorted([v for v in Charging.objects.filter(valid=True).all() if v.still_valid()],
                        key=lambda _: _.start_time)
        first_time = min((l.start_time for l in latest))
        first = [c for c in latest if c.start_time == first_time][0]

        all_ = TeslaTokens.objects.filter(smart_charging=True).all()

        if first.start_time <= datetime.datetime.now(tz=pytz.timezone("Europe/Stockholm")) <= first.end_time:
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
                tokens.stop_charging_all(force=False)
            self.stdout.write(self.style.SUCCESS(f"Will not start charging"
                                                 f" before {first.start_time}"))