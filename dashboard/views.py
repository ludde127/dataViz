from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

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
    plots = data.plottingsetup_set.all()

    return context_render(request, "dashboard/plot.html", context={"title": "plot", "plots": plots,
                                                                   "data_store": data})


@login_required
def secrets_for_data_store(request, public_key: str):
    data_store = get_object_or_404(DataStorage, key=public_key)
    if data_store.owner.user == request.user:
        return context_render(request, "dashboard/secret_key.html", context={"data_store": data_store})
    return HttpResponse("You are not authenticated.")