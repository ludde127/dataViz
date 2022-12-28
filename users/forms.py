from django.core.exceptions import ValidationError
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=64, widget=forms.PasswordInput)

    def is_valid(self):
        valid = super().is_valid()

        psw_match = self.data["password"] == self.data["confirm_password"]
        if not psw_match:
            return False
            #raise ValidationError("The passwords did not match each other.", code="invalid")
        return valid and psw_match


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)