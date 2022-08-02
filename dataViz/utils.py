from django.shortcuts import render
from .settings import BASE_CONTEXT


def context_render(request, template, context=None, *args, **kwargs):
    """Wrapper which injects the base contexts from the settings file."""
    if context is None:
        context = dict()
    context.update(BASE_CONTEXT)
    return render(request, template, context, *args, **kwargs)