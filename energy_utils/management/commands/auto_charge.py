import time

import pytz
from django.core.management.base import BaseCommand
from energy_utils.models import TeslaTokens, scheduled_charging
import datetime


class Command(BaseCommand):
    help = 'Checks if charging should be started.'

    def handle(self, *args, **options):
        first = scheduled_charging()

        if first is not None and first.mean_price < 300:

            all_ = TeslaTokens.objects.filter(smart_charging=True).all()
            for v in all_:
                v.all_vehicles(client=None)  # This will need to be fixed to scala SCALE_ISSUE
            self.stdout.write(self.style.SUCCESS(f"Will sleep to wake all the vehicles."))
            time.sleep(10)
            if first.start_time <= datetime.datetime.now(tz=pytz.UTC) <= first.end_time:  # UTC AS IT WAS TIMESTAMPS
                e = 0
                n = 0
                for tokens in all_:
                    try:
                        tokens.start_charging_all()
                        n += 1
                    except Exception as _e:
                        self.stdout.write(self.style.ERROR(_e))
                        e += 1
                self.stdout.write(self.style.SUCCESS(f"Ran the charging script, started charging for"
                                                     f" {n}/{len(all_)} with {e} errors."))
            else:
                for tokens in all_:
                    tokens.stop_charging_all(force=False)
                self.stdout.write(self.style.SUCCESS(f"Will not start charging"
                                                     f" before {first.start_time.astimezone(tz=pytz.timezone('Europe/Stockholm'))}"))
        else:
            self.stdout.write(self.style.ERROR("No time is scheduled"))