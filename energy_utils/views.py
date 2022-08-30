from pprint import pprint

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from energy_utils.models import TeslaTokens, scheduled_charging
from dataViz.utils import context_render
from .forms import TeslaTokenForm


# Create your views here.
def energy_index(request):
    is_charging = False

    if request.method == "GET":
        schedule_charging = scheduled_charging()

        if request.user.is_authenticated:
            try:
                tesla_token = TeslaTokens.objects.get(owner=request.user.normaluser)
            except TeslaTokens.DoesNotExist:
                tesla_token = TeslaTokens.objects.create(owner=request.user.normaluser)
            if not tesla_token.has_expired():
                try:
                    is_charging = tesla_token.is_charging()
                except requests.exceptions.HTTPError:
                    # Tesla is weird
                    is_charging = None
                    messages.error(request, "We could not connect to the vehicle try again later.")
        else:
            tesla_token = None
        return context_render(request, "energy_utils/index.html",
                              context={"tesla_token": tesla_token, "title": "Energy Utilities",
                                       "tesla_form": TeslaTokenForm() if tesla_token is not None else None,
                                       "tesla_url_token_generation":
                                           None if tesla_token is None
                                           else tesla_token.get_url_for_token_creation(),
                                       "is_charging": is_charging,
                                       "timeOutError": is_charging is None,
                                       "scheduled": schedule_charging
                                       })
    elif request.method == "POST":
        if request.user.is_authenticated:
            form = TeslaTokenForm(request.POST)
            tesla_token = TeslaTokens.objects.get(owner=request.user.normaluser)
            if not tesla_token.has_expired():
                is_charging = tesla_token.is_charging()

            if form.is_valid():
                tesla_token.smart_charging = str(form.cleaned_data["smart_charging"])
                tesla_token.create_tokens(str(form.cleaned_data["secret_url"]))
                messages.success(request, "Token successfully added.")
            else:
                return context_render(request, "energy_utils/index.html",
                                      context={"tesla_token": tesla_token, "title": "Energy Utilities",
                                               "tesla_form": form if tesla_token is not None else None,
                                               "tesla_url_token_generation":
                                                   None if tesla_token.token or tesla_token is None
                                                   else tesla_token.get_url_for_token_creation(),
                                               "is_charging": is_charging,
                                               "scheduled": scheduled_charging()
                                               })
        else:
            messages.error(request, "You are not logged in.")
        return redirect("energy_index")


@login_required
def start_charging(request):
    tok = get_object_or_404(TeslaTokens, owner=request.user.normaluser)
    tok.start_charging_all()
    return redirect("energy_index")


@login_required
def stop_charging(request):
    tok = get_object_or_404(TeslaTokens, owner=request.user.normaluser)
    tok.stop_charging_all()
    return redirect("energy_index")


@login_required
def delete_tesla_tokens(request):
    tok = get_object_or_404(TeslaTokens, owner=request.user.normaluser)
    tok.token = None
    tok.refresh_token = None
    tok.verifier = None
    tok.expiry = 0
    tok.save()
    messages.success(request, "The tokens have been deleted.")
    return redirect("energy_index")