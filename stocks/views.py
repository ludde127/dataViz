from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse

from dataViz.utils import context_render
from .forms import Trade
from .models import Trades

@login_required
def index(request):
    trades = list(Trades.objects.all())
    context = {"trades": trades, "form": Trade()}
    return context_render(request, "stocks/stock_view.html", context)


@login_required
def stock_api(request):
    if request.method == "POST":
        form = Trade(request.POST)
        if form.is_valid():
            Trades.objects.create(stock=form.cleaned_data["stock"], is_buy=form.cleaned_data["is_buy"], owner=request.user.normaluser)
            return HttpResponseRedirect(reverse(index))
    return HttpResponseNotFound("Failed")