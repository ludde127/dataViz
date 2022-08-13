from django.forms import ModelForm
from content.models import Content


class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ["title", "text", "image", "video"]