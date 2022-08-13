from django.forms import ModelForm
from .models import BaseBlock


class BlockForm(ModelForm):
    class Meta:
        model = BaseBlock
        fields = ["human_identifiable_id", "title", "text", "image"]