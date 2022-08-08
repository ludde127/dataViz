from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from dataViz.utils import context_render
from dashboard.models import PlottingSetup, DataStorage
from dashboard.forms import PlottingSetupForm
from data.forms import DataStorageForm
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        if request.method == "POST" and request.user.is_authenticated:
            owner = DataStorage(owner=request.user.normaluser)
            dsf = DataStorageForm(request.POST, instance=owner)
            if dsf.is_valid():
                dsf.save(commit=True)
            else:
                messages.error(request, "Could not save datastore.")
            return redirect("index")

        return context_render(request, "dashboard/index.html",
                              {"title": "Home",
                               "data_stores": DataStorage.objects.filter(owner=request.user.normaluser).all(),
                               "form": DataStorageForm()})
    else:
        if request.method == "POST":
            messages.error(request, "You can not add a datastore as you are not logged in.")
        return context_render(request, "dashboard/index.html",
                              {"title": "Home", "data_stores": None})


def plot(request, key):
    data = get_object_or_404(DataStorage, key=key)
    if request.method == "POST" and request.user.is_authenticated:
        # Plot settings
        psf = PlottingSetupForm(request.POST, instance=PlottingSetup(data=data))
        if psf.is_valid():
            psf.save()
        else:
            messages.error(request, "Could not save the plotting setup form")
        return redirect("plot", key=key)

    plots = data.plottingsetup_set.all()

    return context_render(request, "dashboard/plot.html", context={"title": "plot", "plots": plots,
                                                                   "data_store": data,
                                                                   "form": PlottingSetupForm()})


@login_required
def secrets_for_data_store(request, public_key: str):
    data_store = get_object_or_404(DataStorage, key=public_key)
    if data_store.owner.user == request.user:
        return context_render(request, "dashboard/secret_key.html", context={"data_store": data_store})
    return HttpResponse("You are not authenticated.")