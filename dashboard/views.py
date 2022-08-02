from django.shortcuts import render
from dataViz.utils import context_render
# Create your views here.


def index(request):
    return context_render(request, "dashboard/index.html", {"title": "Home"})