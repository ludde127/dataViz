import json

import pandas as pd
from django.core.exceptions import ValidationError
from django.db import models

from data.models import DataStorage
from users.models import Permissions

background_colors = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(255, 206, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)'
]
border_colors = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(255, 206, 86, 1)',
    'rgba(75, 192, 192, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)'
]


class Plot:
    def __init__(self, datastore: DataStorage, plot_type,
                 title_label,
                 dataframe,
                 _background_colors=None,
                 _border_colors=None, round_index=True, index_is_time=False):
        self.datastore = datastore

        self.plot_type = plot_type
        self.title_label = title_label
        self.df = dataframe
        self.index_is_time = index_is_time
        num_columns = len(self.df.columns)
        if _background_colors is not None:
            self.background_colors = _background_colors
        else:
            self.background_colors = background_colors[
                                     :num_columns if
                                     num_columns < len(background_colors) else len(background_colors)]

        if _border_colors is not None:
            self.border_colors = _border_colors
        else:
            self.border_colors = border_colors[
                                 :num_columns if
                                 num_columns < len(border_colors) else len(border_colors)]
        if round_index:
            self.df.index = map(round, self.df.index)
        if index_is_time and self.datastore.rows > 500:
            self.df = self.df.resample("30T").mean()
        elif self.datastore.rows > 500:
            self.df = self.df.groupby(self.df.index).mean()
        self.df.sort_index(inplace=True)

    def json(self):
        head_dictionary = dict()

        head_data = {"labels": [str(t) for t in self.df.index], "datasets": [
            {
                "pointRadius": 1,
                "data": self.df[column_name].to_list(), "label": column_name,
                "backgroundColor": self.background_colors[n % len(background_colors)],
                "borderColor": self.border_colors[n % len(self.border_colors)
                                                  ]} for n, column_name in enumerate(self.df.columns)]
                     }
        head_dictionary["data"] = head_data
        head_dictionary["type"] = self.plot_type

        head_dictionary["options"] = {
            "plugins": {
                "title": {
                    "display": False,
                    "text": self.datastore.name if self.datastore.name else self.datastore.key,
                }
            },
            "scales": {
                "xAxes": [{
                    "display": True,
                    "scaleLabel": {
                        "display": True,
                        "labelString": self.datastore.index_column
                    },
                }],
            },
        }

        if self.index_is_time:
            head_dictionary["options"]["scales"]["x"] = {"type": 'time',
                                                         "time": {
                                                             "unit": 'hour',
                                                             "displayFormats": {
                                                                 "hour": 'yyyy-MM-dd: HH'
                                                             }
                                                         }}

        return json.dumps(head_dictionary)


# Create your models here.


class PlottingSetup(Permissions):
    data = models.ForeignKey(DataStorage, on_delete=models.CASCADE)

    name = models.CharField("Name for the chart.", max_length=200, default="Unnamed")
    plot_type = models.CharField("Plot type", max_length=35, default="line")

    x_tick_size = models.FloatField("X-Tick", null=True, blank=True)
    y_tick_size = models.FloatField("Y-Tick", null=True, blank=True)

    index_column = models.CharField("Index column (X in graph)", max_length=45)

    columns_to_plot = models.CharField("Columns to plot against X.", max_length=500)

    index_is_time = models.BooleanField("Index is time", default=False)
    round_index = models.BooleanField("Round float index", default=False)

    class Meta:
        unique_together = ["data", "plot_type",
                           "index_column", "columns_to_plot"]

    def __str__(self):
        return f"{self.name} for {self.data.__str__()}"

    def y_columns(self):
        return [s.strip() for s in self.columns_to_plot.split(",")]

    def clean(self):
        if not all((c in self.data.csv_column_names() for c in self.y_columns())):
            raise ValidationError("All the columns to show in Y must exist in the datasets columns.")
        if self.index_column not in self.data.csv_column_names():
            raise ValidationError("The index column must exist in the databases columns.")
        if self.index_is_time and self.round_index:
            raise ValidationError("Rounding of the index is only supported when it is not a time index.")
        return super().clean()

    def plottable(self, plot_last=10000):
        try:
            dataframe = self.data.to_pandas(apply_operations=False)
        except FileNotFoundError:
            return "No data."
        if len(dataframe.values) > plot_last:
            dataframe = dataframe.iloc[-plot_last:]
        dataframe = dataframe.set_index(self.index_column)
        if self.index_is_time:
            try:
                dataframe.index = pd.to_datetime(dataframe.index, unit="s")
            except ValueError:
                dataframe.index = pd.to_datetime(dataframe.index, format='%Y-%m-%d %H:%M:%S.%f')
        for column in dataframe:
            if column not in self.columns_to_plot:
                del dataframe[column]

        return Plot(
            self.data, self.plot_type,
            self.data.key, dataframe, round_index=self.round_index,
            index_is_time=self.index_is_time).json()

    def form(self):
        # This has to be imported locally as PlottingSetupForm depends on this same Model
        from dashboard.forms import PlottingSetupForm
        return PlottingSetupForm(instance=self)
