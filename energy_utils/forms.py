from django import forms


class TeslaTokenForm(forms.Form):
    secret_url = forms.URLField(label="The full url you were redirected to.", required=True)
