from django import forms

class Trade(forms.Form):
    stock = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'placeholder': 'Ticker', 'class': 'form-control'}))
    is_buy = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-select"}), label="", choices=(
            (False, "Sell📉"),
            (True, "Buy📈")
        ))