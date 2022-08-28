from django import forms


class TeslaTokenForm(forms.Form):
    secret_url = forms.URLField(label="The full url you were redirected to.", required=True)
    smart_charging = forms.BooleanField(label="Should we automatically try to charge your vehicle"
                                              " at the cheapest three consecutive hours?")
