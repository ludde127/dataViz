from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from users.models import Permissions
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
        blocks = list(
            itertools.islice(BaseBlock.all_user_can_view(request.user.normaluser, BaseBlock), 10))  # Get 10 first
    else:
        blocks = list(itertools.islice(BaseBlock.objects.filter(public=True), 10))
    return context_render(request, "blocks/index.html", {"title": "Home", "blocks": blocks,
                                                         "form": BlockForm()})


def block(request, hid):
    _block = get_object_or_404(BaseBlock, human_identifiable_id=hid)
    _content = list(itertools.islice(_block.content.filter(Permissions.can_user_view_query(request.user.normaluser)),
                                     25))  # TODO Fix
    url = reverse('add_top_content', kwargs={"block_id": _block.id})
    print(url)
    return context_render(request, "blocks/block.html", {"title": hid, "content": _content,
                                                         "form": ContentForm(), "block_id": _block.id})


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


def delete_block(request, id):
    obj = get_object_or_404(BaseBlock, id=id)
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
            messages.success(request, "Added the wanted block.")
            return redirect("social_index")
        else:
            messages.error(request, "Could not add the block.")
        blocks = list(
            itertools.islice(BaseBlock.objects.filter(Permissions.can_user_view_query(request.user.normaluser)),
                             10))  # Get 10 first

        return context_render(request, "blocks/index.html", {"title": "Home", "blocks": blocks,
                                                             "form": b})


@login_required
def add_top_content(request, block_id):
    if request.method != "POST":
        print("FUCK IFF")
        return HttpResponseNotFound()
    else:
        parent = get_object_or_404(BaseBlock, id=block_id)
        c = ContentForm(request.POST, instance=Content(owner=request.user.normaluser))
        if c.is_valid():
            c = c.save()
            parent.content.add(c)
            parent.save()
            c = ContentForm()
            redirect("block", parent.human_identifiable_id)
        _content = list(
            itertools.islice(parent.content.filter(Permissions.can_user_view_query(request.user.normaluser)),
                             25))  # TODO Fix
        return context_render(request, "blocks/block.html", {"title": parent.human_identifiable_id, "content": _content,
                                                             "form": c, "block_id": block_id})


@login_required
def modify(request, id, is_block):
    is_block = True if is_block == 1 else False
    obj = get_object_or_404(BaseBlock if is_block else Content, id=id, owner=request.user.normaluser)

    if request.method == "POST":
        form = BlockForm(request.POST, instance=obj) if is_block else ContentForm(request.POST, instance=obj)

        if form.is_valid():
            b = form.save()
            messages.success(request, "Successfully made changes.")
            return redirect("content", id) if not is_block else redirect("social_index")
        else:
            messages.error(request, "Could not make changes")
    else:
        form = BlockForm(instance=obj) if is_block else ContentForm(instance=obj)
    return context_render(request, "blocks/modify.html", context={"content": obj, "form": form,
                                                                  "title": "Change", "is_block": is_block})
