from django.http import JsonResponse, HttpResponseBadRequest
from wagtail.search.backends import get_search_backend

from data.models import DataStorage
# Create your views here.
from study_notes.models import NotePage


def search(request):
    if request.GET:
        s = get_search_backend()

        query = request.GET.get("query", None)
        objects = NotePage.objects.live()

        data = {}

        notepages = list(objects.search(query))
        for page in objects.autocomplete(query):
            if page not in notepages:
                notepages.append(page)
        data["Pages"] = [{
            "name": page.title,
            "url": page.get_url(),
            "type": "page"
        } for page in notepages]

        if request.user.is_authenticated:
            data["Datastores"] = [{
                "name": datastore.name,
                "url": datastore.get_url(),
                "type": "datastore"
            } for datastore in s.autocomplete(query,
                                              DataStorage.objects.filter(owner__user=request.user))]

        return JsonResponse(data=data)
    return HttpResponseBadRequest()
