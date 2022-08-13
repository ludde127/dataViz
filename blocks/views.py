from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import BaseBlock, Content
import itertools
from dataViz.utils import context_render
from django.shortcuts import render
from content.forms import ContentForm
from blocks.forms import BlockForm


# Create your views here.


def empty_content_form():
    return ContentForm()


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        blocks = list(itertools.islice(BaseBlock.all_user_can_view(request.user.normaluser, BaseBlock), 10))  # Get 10 first
    else:
        blocks = list(itertools.islice(BaseBlock.objects.filter(public=True), 10))
    return context_render(request, "blocks/index.html", {"title": "Home", "blocks": blocks,
                                                         "form": BlockForm()})


def block(request, hid):
    _block = get_object_or_404(BaseBlock, human_identifiable_id=hid)
    _content = list(itertools.islice(_block.content.all(), 25))  # TODO Fix
    return context_render(request, "blocks/block.html", {"title": hid, "content": _content,
                                                         "empty_content_form": BlockForm()})


def content(request, id):
    _content = get_object_or_404(Content, id=id)
    if request.method == "POST" and request.user.is_authenticated:
        form = ContentForm(request.POST, instance=Content(owner=request.user.normaluser))
        if form.is_valid():
            saved = form.save()
            _content.comments.add(saved)
            _content.save()

            return redirect("content", id=id)
    else:
        form = ContentForm()
    return context_render(request, "blocks/content.html", {"title": _content.title, "content": _content,
                                                           "empty_content_form": form})


def delete_content(request, id):
    obj = get_object_or_404(Content, id=id)
    if request.method != "POST" or not request.user.is_authenticated or not request.user.normaluser == obj.owner:
        return HttpResponseNotFound()
    else:
        if obj.owner == request.user.normaluser:
            obj.safe_delete()
    return redirect("social_index")


@login_required
def add_block(request):
    if request.method != "POST":
        return HttpResponseNotFound()
    else:
        b = BlockForm(request.POST, instance=BaseBlock(owner=request.user.normaluser))
        if b.is_valid():
            b.save()
            return redirect("index")
        return redirect("index")