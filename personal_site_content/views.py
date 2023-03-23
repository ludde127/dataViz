from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.http import require_GET

from .models import TextSection, Page


# Create your views here.
@require_GET
def text_sections(request):
    return HttpResponse(serializers.serialize("json",
                        TextSection.objects.all()),
                        content_type="application/json")

@require_GET
def pages(request):
    return HttpResponse(serializers.serialize("json",
                        Page.objects.all()),
                        content_type="application/json")