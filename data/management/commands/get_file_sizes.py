from django.core.management.base import BaseCommand, CommandError
from data.models import DataStorage, bytes_to_pretty_string


class Command(BaseCommand):
    help = 'Gets the file sizes of all the DataStorages.'

    def handle(self, *args, **options):
        total = 0
        for store in DataStorage.objects.all():
            total += store.read_current_storage_size()
        self.stdout.write(self.style.SUCCESS(f"Checked all the file sizes."
                                             f" Total storage size is {bytes_to_pretty_string(total)}"))