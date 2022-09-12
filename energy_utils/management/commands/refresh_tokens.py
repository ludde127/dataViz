from django.core.management.base import BaseCommand, CommandError
from energy_utils.models import TeslaTokens
import datetime


class Command(BaseCommand):
    help = 'Refreshes all the tesla tokens'

    def handle(self, *args, **options):
        all_ = TeslaTokens.objects.all()
        e = 0
        n = 0
        for tokens in all_:
            if tokens.seconds_until_expiry() < 60*30:
                try:
                    tokens.refresh_tokens()
                except Exception as _e:
                    print(_e)
                    e += 1
                else:
                    n += 1
        self.stdout.write(self.style.SUCCESS(f"Ran the refreshing script, refreshed {n}/{len(all_)} with {e} errors."))