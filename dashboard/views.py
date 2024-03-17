from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

from dashboard.forms import PlottingSetupForm
from dashboard.models import PlottingSetup, DataStorage
from data.forms import DataStorageForm
from dataViz.utils import context_render


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

    psf = PlottingSetupForm(request.POST, instance=PlottingSetup(data=data, owner=request.user.normaluser))

    if request.method == "POST" and request.user.normaluser == data.owner:
        # Plot settings
        if psf.is_valid():
            try:
                psf.save()
                return redirect("plot", key=key)
            except IntegrityError as e:
                messages.error(request, "Failed to create the plot!")
        else:
            messages.error(request, "Failed to create the plot:" + str(psf.errors))

    if data.public or (
            request.user.is_authenticated and request.user.normaluser == data.owner) or data.is_whitelist and request.user.normaluser in data.subjects:
        plots = data.plottingsetup_set.all()
        return context_render(request, "dashboard/plot.html", context={"title": "plot", "plots": plots,
                                                                       "data_store": data,
                                                                       "form": psf})
    else:
        messages.error(request, "You do not have the required permissions")
        return redirect("index")


@login_required
@require_POST
def modify_datastore(request, key):
    data = get_object_or_404(DataStorage, key=key, owner=request.user.normaluser)
    form = DataStorageForm(request.POST, instance=data)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully modified the datastore!")
    else:
        messages.error(request, "Failed to modify the datastore!")
    return redirect("index")


@login_required
@require_POST
def modify_plot(request, id):
    plot = get_object_or_404(PlottingSetup, id=id, owner=request.user.normaluser)
    form = PlottingSetupForm(request.POST, instance=plot)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, "Successfully modified the plot!")
        except IntegrityError as e:
            messages.error(request, "Failed to modify the plot!")
    else:
        messages.error(request, "Failed to modify the plot:" + str(form.errors))
    return redirect("plot", key=plot.data.key)


@login_required
@require_POST
def delete_datastore(request, key: str):
    ds = get_object_or_404(DataStorage, key=key)
    n = ds.name
    if request.user.normaluser == ds.owner:
        ds.delete_data()
        ds.delete()
        messages.success(request, f"Deleted the datastore '{n}'.")
    else:
        messages.error(request, f"You are not the owner. Did nothing.")
    return redirect("index")


@login_required
@require_POST
def delete_plot(request, id: int):
    plot = get_object_or_404(PlottingSetup, id=id)
    name = plot.name
    if request.user.normaluser == plot.owner:
        plot.delete()
        messages.success(request, f"Deleted the plot '{name}'.")
    else:
        messages.error(request, f"You are not the owner. Did nothing.")
    return redirect("plot", key=plot.data.key)


@login_required
def get_all_can_view_link(request, key):
    ds = get_object_or_404(DataStorage, key=key)
    if ds.owner == request.user.normaluser:
        all_key = ds.create_all_can_view_key()
        url = reverse('all_can_view', kwargs={'key': key, 'all_can_view_key': all_key})
        messages.success(request,
                         mark_safe(f"Here's the <a class=\"link\" href={url}>public url</a> that anyone can view."))
    else:
        messages.error(request, "You are not the owner.")
    return redirect("plot", key=key)


def plot_all_can_view(request, key, all_can_view_key):
    ds = get_object_or_404(DataStorage, key=key, all_can_view_key=all_can_view_key)

    return context_render(request, "dashboard/plot.html",
                          context={"title": "plot",
                                   "plots": ds.plottingsetup_set.all(),
                                   "data_store": ds,
                                   "shared": True})
