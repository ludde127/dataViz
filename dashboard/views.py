from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from dataViz.utils import context_render
from dashboard.models import PlottingSetup, DataStorage
from dashboard.forms import PlottingSetupForm
from data.forms import DataStorageForm


# Create your views here.


def index(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            owner = DataStorage(owner=request.user.normaluser)
            dsf = DataStorageForm(request.POST, instance=owner)
            if dsf.is_valid():
                dsf = dsf.save(commit=True)

                return redirect("index")

            else:
                messages.error(request, "Could not save datastore.")
        else:
            dsf = DataStorageForm()

        available = DataStorage.all_user_can_view(request.user.normaluser, _class=DataStorage)
        return context_render(request, "dashboard/index.html",
                              {"title": "Home",
                               "data_stores": available.all(),
                               "form": dsf})
    else:
        if request.method == "POST":
            messages.error(request, "You can not add a datastore as you are not logged in.")
        return context_render(request, "dashboard/index.html",
                              {"title": "Home", "data_stores": DataStorage.objects.filter(public=True)})


def plot(request, key):
    data = get_object_or_404(DataStorage, key=key)
    if request.method == "POST" and request.user.normaluser == data.owner:
        # Plot settings
        psf = PlottingSetupForm(request.POST, instance=PlottingSetup(data=data, owner=request.user.normaluser))
        if psf.is_valid():
            psf.save()
            return redirect("plot", key=key)
        else:
            messages.error(request, "Could not save the plotting setup form")
    if data.public or (request.user.is_authenticated and request.user.normaluser == data.owner) or\
            data.is_whitelist and request.user.normaluser in data.subjects:
        plots = data.plottingsetup_set.all()

        return context_render(request, "dashboard/plot.html", context={"title": "plot", "plots": plots,
                                                                       "data_store": data,
                                                                       "form": PlottingSetupForm()})
    else:
        messages.error(request, "You do not have the required permissions")
        return redirect("index")


@login_required
def secrets_for_data_store(request, public_key: str):
    data_store = get_object_or_404(DataStorage, key=public_key)
    if data_store.owner.user == request.user:
        return context_render(request, "dashboard/secret_key.html", context={"data_store": data_store})
    return HttpResponse("You are not authenticated.")


@login_required
def modify_datastore(request, key):
    data = get_object_or_404(DataStorage, key=key, owner=request.user.normaluser)
    if request.method == "POST":
        form = DataStorageForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = DataStorageForm(instance=data)
    return context_render(request, "dashboard/modify_datastore.html",
                          context={"title": "Modify Datastorage", "form": form, "data": data})


@login_required
def modify_plot(request, id):
    plot = get_object_or_404(PlottingSetup, id=id, owner=request.user.normaluser)
    if request.method == "POST":
        form = PlottingSetupForm(request.POST, instance=plot)
        if form.is_valid():
            form.save()
            return redirect("plot", key=plot.data.key)
    else:
        form = PlottingSetupForm(instance=plot)
    return context_render(request, "dashboard/modify_plot.html", context={"title": "Modify Plot",
                                                                          "form": form, "old": plot})


@login_required
def delete_datastore(request, key:str):
    ds = get_object_or_404(DataStorage, key=key)
    n = ds.name
    if request.user.normaluser == ds.owner:
        ds.delete_data()
        ds.delete()
        messages.info(request, f"Deleted the datastore '{n}'.")
    else:
        messages.error(request, f"You are not the owner. Did nothing.")
    return redirect("index")


@login_required
def get_all_can_view_link(request, key):
    ds = get_object_or_404(DataStorage, key=key)
    if ds.owner == request.user.normaluser:
        all_key = ds.create_all_can_view_key()
        url = reverse('all_can_view', kwargs={'key': key, 'all_can_view_key': all_key})
        messages.success(request, mark_safe(f"All can view <a href={url}>url</a>"))
    else:
        messages.error(request, "You are not the owner.")
    return redirect("plot", key=key)


def plot_all_can_view(request, key, all_can_view_key):
    ds = get_object_or_404(DataStorage, key=key, all_can_view_key=all_can_view_key)

    return context_render(request, "dashboard/plot.html",
                          context={"title": "plot", "plots": ds.plottingsetup_set.all(), "data_store": ds,
                                   "shared": True})