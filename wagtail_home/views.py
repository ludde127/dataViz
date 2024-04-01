from django.http import JsonResponse, HttpResponseBadRequest
from wagtail.search.backends import get_search_backend
from wagtail.search.utils import parse_query_string

from data.models import DataStorage
# Create your views here.
from study_notes.models import NotePage, NotePageTag
from users.models import NormalUser

s = get_search_backend()


def _search_and_autocomplete(*args):
    search_results = list(s.search(*args, operator="OR"))
    for result in s.autocomplete(*args, operator="OR"):
        if result not in search_results:
            search_results.append(result)
    return search_results


def search(request):
    if request.GET:
        query = request.GET.get("query", None)
        filters, query = parse_query_string(query)

        data = dict()

        live_pages = NotePage.objects.live()
        author_filter = filters.get("author")
        if author_filter:
            live_pages = live_pages.filter(live_revision__user__username__contains=author_filter)
        data["Pages"] = [{
            "name": page.title,
            "url": page.get_url(),
            "type": "page"
        } for page in _search_and_autocomplete(query, live_pages)]

        if request.user.is_authenticated:
            data["Datastores"] = [{
                "name": datastore.name,
                "url": datastore.get_url(),
                "type": "datastore"
            } for datastore in _search_and_autocomplete(query,
                                                        DataStorage.objects.filter(owner__user=request.user))]

        seen_tags = set()
        data["Tags"] = [x for x in [{
            "name": tag.tag.name,
            "url": tag.get_url(),
            "type": "tag"
        } for tag in _search_and_autocomplete(query, NotePageTag)]
                        if not (x["name"] in seen_tags or seen_tags.add(x["name"]))]

        data["Users"] = [{
            "name": user.user.get_username(),
            "url": user.get_url(),
            "type": "user"
        } for user in _search_and_autocomplete(query, NormalUser)]

        return JsonResponse(data=data)
    return HttpResponseBadRequest()
