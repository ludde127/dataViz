from django.core.management import BaseCommand
from tests.utils import run_standard_production_tests


class Command(BaseCommand):
    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def error(self, msg):
        self.stdout.write(self.style.ERROR(msg))

    help = 'This runs tests that can be used in production.'

    def handle(self, *args, **options):
        for result in run_standard_production_tests():
            if result.was_error:
                self.error(result.msg)
            else:
                self.success(result.msg)
