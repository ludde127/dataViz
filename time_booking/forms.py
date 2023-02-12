from django.forms import ModelForm, DateInput
from .models import TimeSlotBooking, TimeSlot
from django import forms


class TimeSlotBookingForm(ModelForm):
    class Meta:
        model = TimeSlotBooking
        fields = ["name", "description"]

class TimeSlotForm(ModelForm):
    time_slot_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs=dict(type='datetime-local')), required=True)
    time_slot_end = forms.DateTimeField(widget=forms.DateTimeInput(attrs=dict(type='datetime-local')), required=True)

    class Meta:
        model = TimeSlot
        fields = ["time_slot_start", "time_slot_end"]