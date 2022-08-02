import uuid
from django.db import models
import json
from dataViz.settings import DATA_FILES
# Create your models here.
from users.models import NormalUser


class DataStorage(models.Model):
    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    csv_names = models.CharField(verbose_name="Names for the csv-files.", max_length=1000)
    key = models.CharField(verbose_name="KEY", default=uuid.uuid4, unique=True, max_length=200) #  TODO MAKE THIS ACTUALLY SAFE

    def file_path(self):
        return DATA_FILES.joinpath(str(self.key)+".csv")

    def csv_column_names(self):
        return [s.strip() for s in self.csv_names.split(",")]

    @staticmethod
    def get_by_key(key):
        return DataStorage.objects.get(key=key)

    def add_data(self, parsed):
        self.assert_json_format(parsed)
        is_multiple = isinstance(parsed[self.csv_names[0]], list)
        try:
            existed = self.file_path().exists()
            with open(self.file_path(), "a+") as f:
                if not existed:
                    line = ",".join(self.csv_column_names())
                    f.write(f"{line}\n")
                if not is_multiple:
                    line = ",".join([str(parsed[key]) for key in self.csv_column_names()])
                    f.write(f"{line}\n")
                else:
                    length = len(parsed[self.csv_names[0]])
                    for i in range(length):
                        line = ",".join([str(parsed[key][i]) for key in self.csv_column_names()])
                        f.write(f"{line}\n")
        except FileNotFoundError:
            import os
            os.makedirs(self.file_path().parent)
            self.add_data(parsed)

    def get_all_data(self):
        if self.file_path().exists():
            with open(self.file_path(), "r") as f:
                data = f.readlines()
            return "\n".join(data)
        return ""

    def assert_json_format(self, parsed_json):
        missing = list()
        for name in self.csv_column_names():
            if name not in parsed_json.keys():
                missing.append(str(name))
        if len(missing) > 0:
            raise AssertionError("Some of the specified data "
                                 "names where missing: " + str(missing))
