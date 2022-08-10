import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from dataViz.settings import DATA_FILES
# Create your models here.
from users.models import NormalUser, Permissions
from os import path as os_path
import secrets
import pandas as pd

BYTES_PER_GB = 1024**3
BYTES_PER_MB = 1024**2
BYTES_PER_KB = 1024


def bytes_to_pretty_string(bytes: float) -> str:
    if bytes > BYTES_PER_GB/10:
        return f"{round(bytes/BYTES_PER_GB, 3)} GB"
    elif bytes > BYTES_PER_MB/10:
        return f"{round(bytes/BYTES_PER_MB, 3)} MB"
    elif bytes > BYTES_PER_KB/10:
        return f"{round(bytes/BYTES_PER_KB, 3)} KB"
    else:
        return f"{round(bytes)} Bytes"


def make_secret_key():
    return secrets.token_urlsafe(32)


class DataStorage(Permissions):
    csv_names = models.CharField(verbose_name="Data column names (ex. 'time, velocity, position')", max_length=1000)
    key = models.CharField(verbose_name="KEY", default=uuid.uuid4, unique=True, max_length=200) #  TODO MAKE THIS ACTUALLY SAFE

    rows = models.IntegerField(verbose_name="Amount of rows", default=0)
    storage_size = models.IntegerField(verbose_name="Storage Size (Bytes)", default=0)

    name = models.CharField(verbose_name="Name", max_length=100, null=False, unique=True)
    description = models.TextField(verbose_name="Description", max_length=3000, null=True, blank=True)

    secret_key = models.CharField(verbose_name="Secret Api Key", editable=False,
                                  default=make_secret_key, unique=True, max_length=64)

    index_column = models.CharField(verbose_name="Index column", default=None, max_length=30, blank=True, null=True)
    index_column_values_are_time = models.BooleanField(verbose_name="Index is a time format", default=True)

    def clean(self):
        if self.index_column not in self.csv_column_names():
            raise ValidationError("The index must be one of the columns.")
        if self.index_column is None and self.index_column_values_are_time:
            raise ValidationError("A null index cant be a time index.")
        return super().clean()

    def __str__(self):
        return f"{self.name} - {self.owner}"

    def valid_authorization(self, request):
        try:
            auth = str(request.environ.get('HTTP_AUTHORIZATION'))  # Gives TOK:<mAmq8-3c880bMCmxy_LQkUJy18r4-uR09zvu0tLEDz4>
            if "TOK" in auth:
                auth = auth.split(":")[-1].replace("<", "").replace(">","")
        except KeyError:
            raise ValueError("You must set the http authorization header to your secret api key")
        print(auth)
        return auth == self.secret_key

    def file_path(self):
        return DATA_FILES.joinpath(str(self.key)+".csv")

    def csv_column_names(self):
        return [s.strip() for s in self.csv_names.split(",")]

    def read_current_storage_size(self):
        if self.file_path().exists():
            self.storage_size = round(os_path.getsize(str(self.file_path())))  # Get file size in bytes
        else:
            self.storage_size = 0
        self.save()
        return self.storage_size

    def storage_size_in_best_format(self) -> str:
        return bytes_to_pretty_string(self.storage_size)

    @staticmethod
    def get_by_key(key):
        return DataStorage.objects.get(key=key)

    def __add_data(self, parsed, file_opening="a+"):
        self.assert_json_format(parsed)

        is_multiple = isinstance(parsed[self.csv_column_names()[0]], list)
        try:
            with open(self.file_path(), file_opening) as f:
                if not is_multiple:
                    line = ",".join([str(parsed[key]) for key in self.csv_column_names()])
                    self.rows += 1
                    f.write(f"{line}\n")
                else:
                    length = len(parsed[self.csv_names[0]])
                    for i in range(length):
                        line = ",".join([str(parsed[key][i]) for key in self.csv_column_names()])
                        self.rows += 1
                        f.write(f"{line}\n")
        except FileNotFoundError:
            import os
            os.makedirs(self.file_path().parent)
            self.add_data(parsed)
        self.save()

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

    def to_pandas(self, apply_operations=True):
        """Loads it and converts the index to datetime if it is indeed a time index."""
        df = pd.read_csv(self.file_path(), index_col=False, names=self.csv_column_names())
        if apply_operations:
            if self.index_column and self.index_column_values_are_time:
                df[self.index_column] = pd.to_datetime(df[self.index_column], unit="s")
            if self.index_column:
                df = df.set_index(self.index_column)
        return df

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
                                 "names where missing: " + str(missing) + " The existing where " + str(parsed_json.keys()))
