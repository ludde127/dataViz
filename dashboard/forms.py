from django.forms import ModelForm
from dashboard.models import PlottingSetup


class PlottingSetupForm(ModelForm):
    class Meta:
        model = PlottingSetup
        fields = ["name", "plot_type", "columns_to_plot", "index_column", "index_is_time",
                  "round_index", "x_tick_size", "y_tick_size"]
