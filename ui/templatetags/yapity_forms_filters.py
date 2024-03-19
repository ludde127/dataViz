from django import forms
from django.forms import ModelForm

from tags.templatetags import register
from ui.widgets import CheckboxSelectMultipleWOA


@register.filter(name="yapity_form")
def as_yapity_form(form: ModelForm):
    for name in form.fields:
        field = form.fields[name]
        if isinstance(field.widget, forms.TextInput) or isinstance(field.widget, forms.Textarea) or isinstance(
                field.widget, forms.PasswordInput) or isinstance(field.widget, forms.EmailInput):
            field.widget.attrs.update({'class': 'input input-bordered'})
        elif isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.update({'class': 'toggle'})
        elif isinstance(field.widget, forms.NumberInput):
            field.widget.attrs.update({'class': 'input input-bordered'})
        elif isinstance(field.widget, forms.Select):
            field.widget.attrs.update({'class': 'select select-bordered'})
        elif isinstance(field.widget, CheckboxSelectMultipleWOA):
            pass
        else:
            print("Un-styled input field:", type(field), type(field.widget))

    return form
