import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404
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

@require_GET
def page(request, page):

    page_obj: Page = get_object_or_404(Page, pk=page)
    data = {
        "page": json.loads(serializers.serialize("json", [page_obj]))[0],
        "textSections": json.loads(serializers.serialize("json", list(page_obj.textsection_set.all()))),
        "test": 1
    }
    return JsonResponse(data=data, content_type="application/json")

