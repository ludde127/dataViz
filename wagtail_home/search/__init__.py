#https://docs.wagtail.org/en/stable/topics/search/searching.html#an-example-page-search-view
from wagtail.search.backends import get_search_backend
from study_notes.models import NotePage

s = get_search_backend()
s.search("datorkom", NotePage)