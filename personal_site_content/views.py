from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import TextSection


# Create your views here.
@require_GET
def text_sections(request):
    return HttpResponse(serializers.serialize("json", TextSection.objects.all()), content_type="application/json")