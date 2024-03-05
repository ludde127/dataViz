from django.http import JsonResponse, HttpResponseBadRequest
# Create your views here.
from study_notes.models import NotePage


def search(request):
    if request.GET:
        query = request.GET.get("query", None)
        objects = NotePage.objects.live()

        result = list(objects.search(query))
        for auto in objects.autocomplete(query):
            if auto not in result:
                result.append(auto)

        return JsonResponse(data={"results": [{"title": res.title, "url": res.get_url()} for res in result]})
    return HttpResponseBadRequest()
