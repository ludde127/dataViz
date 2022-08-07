from django.shortcuts import get_object_or_404

from .models import BaseBlock, Content
import itertools
from dataViz.utils import context_render


# Create your views here.
def index(request):
    blocks = list(itertools.islice(BaseBlock.get_viewable(request), 10))  # Get 10 first
    return context_render(request, "blocks/index.html", {"title": "Home", "blocks": blocks})


def block(request, hid):
    _block = get_object_or_404(BaseBlock, human_identifiable_id=hid)
    _content = list(itertools.islice(_block.content.all(), 25)) # TODO Fix
    return context_render(request, "blocks/block.html", {"title": hid, "content": _content})


def content(request, id):
    _content = get_object_or_404(Content, id=id)
    return context_render(request, "blocks/content.html", {"title": _content.title, "content": _content})