# forms.py

from django import forms
from django.contrib.auth import get_user_model

class CustomSettingsForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = []