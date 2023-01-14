from tags.templatetags import register
from wagtail_home.customizations.converters.utils import render_markdown


@register.filter(name="markdown")
def markdown(value):
    return render_markdown(value)
