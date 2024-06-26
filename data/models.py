import datetime
import os
import secrets
import uuid
from os import path as os_path

import pandas as pd
from django.core.exceptions import ValidationError
from django.db import models
from django.http import QueryDict
from django.urls import reverse
from wagtail.search import index

from dataViz.settings import DATA_FILES
# Create your models here.
from users.models import Permissions

BYTES_PER_GB = 1024 ** 3
BYTES_PER_MB = 1024 ** 2
BYTES_PER_KB = 1024


class InconstantTypes:
    pass


def bytes_to_pretty_string(bytes: float) -> str:
    if bytes > BYTES_PER_GB / 10:
        return f"{round(bytes / BYTES_PER_GB, 3)} GB"
    elif bytes > BYTES_PER_MB / 10:
        return f"{round(bytes / BYTES_PER_MB, 3)} MB"
    elif bytes > BYTES_PER_KB / 10:
        return f"{round(bytes / BYTES_PER_KB, 3)} KB"
    else:
        return f"{round(bytes)} Bytes"


def make_secret_key():
    return secrets.token_urlsafe(32)


def float_timestamp_to_dt(v: float) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(v)


class DataStorage(Permissions, index.Indexed):
    csv_names = models.CharField(verbose_name="Data column names (ex. 'time, velocity, position')", max_length=1000)
    key = models.CharField(verbose_name="KEY", default=uuid.uuid4, unique=True,
                           max_length=200)  # TODO MAKE THIS ACTUALLY SAFE

    rows = models.IntegerField(verbose_name="Amount of rows", default=0)
    storage_size = models.IntegerField(verbose_name="Storage Size (Bytes)", default=0)

    name = models.CharField(verbose_name="Name", max_length=100, null=False, unique=True)
    description = models.TextField(verbose_name="Description", max_length=3000, null=True, blank=True)

    secret_key = models.CharField(verbose_name="Secret Api Key", editable=True,
                                  default=make_secret_key, unique=True, max_length=64)

    index_column = models.CharField(verbose_name="Index column", default=None, max_length=30, blank=True, null=True)
    index_column_values_are_time = models.BooleanField(verbose_name="Index is a time format", default=True)
    all_can_view_key = models.UUIDField(default=uuid.uuid4)

    search_fields = [
        index.SearchField('name'),
        index.AutocompleteField('name'),
        index.SearchField('description'),
        index.AutocompleteField('description'),
        index.AutocompleteField('csv_names'),
        index.FilterField('user_id'),
    ]

    def clean(self):
        if self.index_column not in self.csv_column_names():
            raise ValidationError("The index must be one of the columns.")
        if self.index_column is None and self.index_column_values_are_time:
            raise ValidationError("A null index cant be a time index.")
        return super().clean()

    def __str__(self):
        return f"{self.name} - {self.owner}"

    def get_url(self):
        return reverse('plot', kwargs={'key': self.key})

    def valid_authorization(self, request):
        try:
            auth = str(
                request.environ.get('HTTP_AUTHORIZATION'))  # Gives TOK:<mAmq8-3c880bMCmxy_LQkUJy18r4-uR09zvu0tLEDz4>
            if "TOK" in auth:
                auth = auth.split(":")[-1].replace("<", "").replace(">", "")
        except KeyError:
            raise ValueError("You must set the http authorization header to your secret api key")
        return auth == self.secret_key

    def file_path(self):
        return DATA_FILES.joinpath(str(self.key) + ".csv")

    def form(self):
        # This has to be imported locally as DataStorageForm depends on this same Model
        from data.forms import DataStorageForm
        return DataStorageForm(instance=self)

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

    def __add_data(self, parsed: QueryDict, file_opening="a+"):
        if isinstance(parsed, QueryDict):
            parsed = {k: v for (k, v) in list(parsed.lists())}  # This turns it into the form i would expect -->
        elif isinstance(parsed, dict):

            parsed = {k: [v, ] for k, v in parsed.items()}
        # {'a': ['2020-12-01'], 'b': ['10'], 'c': ['14']}
        # OR {'a': ['2020-12-01', 'asda'], 'b': ['10', '2'], 'c': ['14', '3']} etc

        self.assert_json_format(parsed)
        try:
            with open(self.file_path(), file_opening) as f:
                length = len(parsed[self.csv_column_names()[0]])

                lines = []
                for i in range(length):
                    line = ",".join([str(parsed[key][i]) for key in self.csv_column_names()])
                    self.rows += 1
                    lines.append(line.strip() + "\n")
                f.writelines(lines)
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
        print(data)
        return "".join(data)

    def to_pandas(self, apply_operations=True):
        """Loads it and converts the index to datetime if it is indeed a time index."""
        df = pd.read_csv(self.file_path(), index_col=False, names=self.csv_column_names())

        if apply_operations:
            if self.index_column and self.index_column_values_are_time:
                df[self.index_column] = pd.to_datetime(df[self.index_column], unit="s")
                print(df[self.index_column])
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
                                 "names where missing: " + str(missing) + " The existing where " + str(
                parsed_json.keys()))

    def latest_row(self):
        if not self.file_path().exists():
            return None
        with open(self.file_path(), 'rb') as f:
            try:  # catch OSError in case of a one line file
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()

        def to_datetime_if_time_index(n, v):
            if n == self.index_column and self.index_column_values_are_time:
                try:
                    timestamp = int(float(v))
                except TypeError:
                    # https://stackabuse.com/converting-strings-to-datetime-in-python/
                    date_time_obj = datetime.datetime.strptime(str(v), '%Y-%m-%d %H:%M:%S.%f')
                    timestamp = int(date_time_obj.timestamp())
                return n, float_timestamp_to_dt(timestamp)
            return n, v

        return ", ".join([f"{n}: {v}" for n, v in
                          (to_datetime_if_time_index(n, v) for n, v in zip(self.csv_column_names(),
                                                                           last_line.split(",")))])

    def stream(self):
        """Streams the data row-wise split into a list for each column"""
        if self.file_path().exists():
            with open(self.file_path(), "r") as file:
                while line := file.readline():
                    yield line.split(",")
        yield StopIteration

    def constant_types(self):
        """Returns a dictionary with column_name:type key-value pairs if
         the types are constant troughout all the columns. If a column has inconsistent types that column gets
          the class InconstantTypes"""

        types = dict()
        first = True
        for row_values in self.stream():
            if first:
                types = {k: type(v) for k, v in zip(self.csv_column_names(), row_values)}
            else:
                for key, val in zip(self.csv_column_names(), row_values):
                    if type(val) != types[key]:
                        types[key] = InconstantTypes
            first = False
        return types

    def example_entry(self):
        index = self.index_column
        t = self.index_column_values_are_time

        def placeholder(column: str):
            if column == index and t:
                return "Time_either_unix_seconds_or_datetime_OSI8601"
            elif column == index:
                return "IndexValue"
            else:
                return "SomeValue"

        return {k: placeholder(k) for k in self.csv_column_names()}.__repr__()

    def create_all_can_view_key(self):
        self.all_can_view_key = uuid.uuid4()
        self.save()
        return self.all_can_view_key
