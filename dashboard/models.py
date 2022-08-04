import json
from pprint import pprint

from django.db import models
from data.models import DataStorage

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
                 labels=None,
                 _background_colors=None,
                 _border_colors=None):
        self.datastore = datastore

        self.plot_type = plot_type
        self.title_label = title_label

        if labels is not None:
            self.labels = labels
            self.use_first_col_as_labels = False
        else:
            self.labels = self.datastore.column_wise()[0]
            self.use_first_col_as_labels = True
        number_labels = len(self.labels)

        if _background_colors is not None:
            self.background_colors = _background_colors
        else:
            self.background_colors = background_colors[
                                     :number_labels if
                                     number_labels < len(background_colors) else len(background_colors)]

        if _border_colors is not None:
            self.border_colors = _border_colors
        else:
            self.border_colors = border_colors[
                                 :number_labels if
                                 number_labels < len(border_colors) else len(border_colors)]

    def json(self):
        head_dictionary = dict()

        head_data = {"labels": self.labels[1], "datasets": [
            {
                "data": column_values, "label": column_name,
                "backgroundColor": self.background_colors[n % len(background_colors)],
                "borderColor": self.border_colors[n % len(self.border_colors)
                                                  ]} for n, (column_name, column_values) in
            enumerate(
                self.datastore.column_wise() if not self.use_first_col_as_labels else self.datastore.column_wise()[1:])
        ]}
        head_dictionary["data"] = head_data
        head_dictionary["type"] = self.plot_type

        head_dictionary["options"] = {"plugins": {
            "title": {
                "display": True,
                "text": self.datastore.key,
            }},
            "scales": {
                "xAxes": [{
                    "display": True,
                    "scaleLabel": {
                        "display": True,
                        "labelString": self.datastore.csv_column_names()[0] if self.use_first_col_as_labels else "Index"
                    }
                }]
            }
        }

        pprint(head_dictionary)
        return json.dumps(head_dictionary)


# Create your models here.


class PlottingSetup(models.Model):
    data = models.OneToOneField(DataStorage, on_delete=models.PROTECT)

    plot_type = models.CharField("Plot type", max_length=35, default="line")
    labels = models.CharField("Labels", max_length=500, null=True, blank=True)
    x_tick_size = models.FloatField("X-Tick", null=True, blank=True)
    y_tick_size = models.FloatField("Y-Tick", null=True, blank=True)

    def plottable(self):
        return Plot(
            self.data, self.plot_type,
            self.data.key).json()
