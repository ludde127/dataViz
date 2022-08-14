from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import BaseBlock
from django.utils.translation import gettext as _


class BlockForm(ModelForm):
    class Meta:
        model = BaseBlock
        fields = ["human_identifiable_id", "title", "text", "image"]

    def clean_human_identifiable_id(self):
        if " " in self.cleaned_data["human_identifiable_id"]:
            return ValidationError(_("The display name may not contain spaces."), code='invalid')
        return self.cleaned_data["human_identifiable_id"]
