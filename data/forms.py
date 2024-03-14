from django.forms import ModelForm
from data.models import DataStorage
from django import forms


class DataStorageForm(ModelForm):
    class Meta:
        model = DataStorage
        fields = ["name", "description", "csv_names",
                  "index_column", "index_column_values_are_time"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered"}),
            "description": forms.TextInput(attrs={"class": "textarea textarea-bordered"}),
            "csv_names": forms.TextInput(attrs={"class": "input input-bordered"}),
            "index_column": forms.TextInput(attrs={"class": "input input-bordered"}),
            "index_column_values_are_time": forms.CheckboxInput({"class": "toggle"}),
        }
