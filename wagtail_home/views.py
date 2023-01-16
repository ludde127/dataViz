from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
# Create your views here.
from wagtail.search.backends import get_search_backend
from study_notes.models import NotePage, NotePageTag
from wagtail.search.models import Query
from django.core import serializers


def search(request):
    if request.GET:
        query = request.GET.get("query", None)
        result = list(NotePage.objects.live().autocomplete(query))
        Query.get(query).add_hit()
        return JsonResponse(data={"results": [{"title": res.title, "url": res.get_url()} for res in result]})
    return HttpResponseBadRequest()