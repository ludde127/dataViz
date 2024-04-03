from django import forms
from django.forms import ModelForm

from dashboard.models import PlottingSetup
from ui.widgets import CheckboxSelectMultipleWOA


class ChoiceSettings:
    def __init__(self, label, **kwargs):
        self.label = label
        self.kwargs = kwargs


class PlottingSetupForm(ModelForm):
    plot_type = forms.ChoiceField(
        choices=[("line", "line")],
        widget=forms.Select,
        label="Plot Type"
    )

    def __init__(self, *args, **kwargs):
        super(PlottingSetupForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields["index_column"] = forms.ChoiceField(
                choices=[(c, c) for c in self.instance.data.csv_column_names()],
                widget=forms.Select,
                label="Index Column (X axis)")

            cols = self.instance.y_columns()
            self.fields["columns_to_plot"] = forms.MultipleChoiceField(
                choices=[(c,
                          ChoiceSettings(c,
                                         **{"class": "toggle",
                                            "checked": c in cols})
                          )
                         for c in self.instance.data.csv_column_names()],
                widget=CheckboxSelectMultipleWOA,
                label="Columns to plot (Y axes)")

    class Meta:
        model = PlottingSetup
        fields = ["name", "plot_type", "index_column", "index_is_time", "round_index",
                  "columns_to_plot",
                  "x_tick_size", "y_tick_size"]

    def clean_columns_to_plot(self):
        data = ",".join(self.cleaned_data["columns_to_plot"])
        self.cleaned_data["columns_to_plot"] = data
        return data
