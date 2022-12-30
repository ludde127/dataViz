import json

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from study_notes.models import NotePage, get_notepage_from_id
from wagtail_home.models import filter_non_viewable

# Create your views here.
def get_flashcards(request, notepage_id: str):
    page: NotePage = get_notepage_from_id(request, notepage_id)
    if page is None:
        return HttpResponseForbidden()
    _json, start, length = page.get_flashcards()
    combined = dict()
    combined["quiz_json"] = _json
    combined["quiz_starts"] = start
    combined["quiz_lengths"] = length

    return HttpResponse(json.dumps(combined), content_type='application/json')
