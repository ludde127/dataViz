from django.shortcuts import render, get_object_or_404
from dataViz.utils import context_render
from dashboard.models import PlottingSetup, DataStorage
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return context_render(request, "dashboard/index.html",
                              {"title": "Home", "data_stores": DataStorage.objects.filter(owner=request.user.normaluser).all()})
    else:
        return context_render(request, "dashboard/index.html",
                              {"title": "Home", "data_stores": None})


def plot(request, key, together=True):
    data = get_object_or_404(DataStorage, key=key)

    if request.method == "POST":
        # Plot settings
        pass
    if hasattr(data, "plottingsetup"):
        if together:
            plottableJSON = data.plottingsetup.plottable_together()
    else:
        _ = PlottingSetup.objects.create(data=data)
        if together:
            plottableJSON = _.plottable_together()
    return context_render(request, "dashboard/plot.html", context={"title": "plot", "chartJSON": plottableJSON})
