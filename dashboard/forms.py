from django import forms
from django.forms import ModelForm

from dashboard.models import PlottingSetup


class PlottingSetupForm(ModelForm):
    class Meta:
        model = PlottingSetup
        fields = ["name", "plot_type", "columns_to_plot", "index_column", "index_is_time",
                  "round_index", "x_tick_size", "y_tick_size"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "input input-bordered"}),
            "plot_type": forms.TextInput(attrs={"class": "input input-bordered"}),
            "columns_to_plot": forms.TextInput(attrs={"class": "input input-bordered"}),
            "index_column": forms.TextInput(attrs={"class": "input input-bordered"}),
            "index_is_time": forms.CheckboxInput({"class": "toggle"}),
            "round_index": forms.CheckboxInput({"class": "toggle"}),
            "x_tick_size": forms.NumberInput(attrs={"class": "input input-bordered"}),
            "y_tick_size": forms.NumberInput(attrs={"class": "input input-bordered"}),
        }
