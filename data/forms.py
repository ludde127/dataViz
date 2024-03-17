from django.forms import ModelForm

from data.models import DataStorage


class DataStorageForm(ModelForm):
    class Meta:
        model = DataStorage
        fields = ["name", "description", "csv_names",
                  "index_column", "index_column_values_are_time"]
