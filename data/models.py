import uuid
from django.db import models
from dataViz.settings import DATA_FILES
# Create your models here.
from users.models import NormalUser


class DataStorage(models.Model):
    owner = models.ForeignKey(NormalUser, on_delete=models.CASCADE)
    csv_names = models.CharField(verbose_name="Names for the csv-files.", max_length=1000)
    key = models.CharField(verbose_name="KEY", default=uuid.uuid4, unique=True, max_length=200) #  TODO MAKE THIS ACTUALLY SAFE

    name = models.CharField(verbose_name="Name", max_length=100, null=False, unique=True)
    description = models.TextField(verbose_name="Description", max_length=3000, null=True)

    def file_path(self):
        return DATA_FILES.joinpath(str(self.key)+".csv")

    def csv_column_names(self):
        return [s.strip() for s in self.csv_names.split(",")]

    @staticmethod
    def get_by_key(key):
        return DataStorage.objects.get(key=key)

    def __add_data(self, parsed, file_opening="a+"):
        self.assert_json_format(parsed)
        is_multiple = isinstance(parsed[self.csv_names[0]], list)
        try:
            existed = self.file_path().exists()
            with open(self.file_path(), file_opening) as f:
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

    def add_data(self, parsed):
        self.__add_data(parsed, "a+")
        self.owner.api_access_count += 1
        self.owner.save()

    def put_data(self, data):
        self.__add_data(data, "w+")
        self.owner.api_access_count += 1
        self.owner.save()

    def delete_data(self):
        if self.file_path().exists():
            with open(self.file_path(), "w") as _:
                pass
            self.owner.api_access_count += 1
            self.owner.save()

    def get_all_data(self):
        data = ""
        if self.file_path().exists():
            with open(self.file_path(), "r") as f:
                data = f.readlines()
        self.owner.api_access_count += 1
        self.owner.save()
        return "\n".join(data)

    def column_wise(self):
        """Returns the data formatted like [(col1, [d1, d2, d3...]), (col2, [d1, d2, d3...])]"""
        data = []
        column_wise = []
        if self.file_path().exists():
            with open(self.file_path(), "r") as f:
                data = f.readlines()

        for row in data:
            for n, col in enumerate(row.split(",")):
                try:
                    column_wise[n][1].append(col)
                except (IndexError, TypeError):
                    column_wise.append((self.csv_column_names()[n], list()))
                    column_wise[n][1].append(col)

        return column_wise

    def assert_json_format(self, parsed_json):
        missing = list()
        for name in self.csv_column_names():
            if name not in parsed_json.keys():
                missing.append(str(name))
        if len(missing) > 0:
            raise AssertionError("Some of the specified data "
                                 "names where missing: " + str(missing))
