import json

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import TimeSlotBooking, TimeSlot
from dataViz.utils import context_render
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from .forms import TimeSlotBookingForm, TimeSlotForm


# Create your views here.
def booking(request, booking_uuid):
    print(booking_uuid)
    try:
        booking_obj = get_object_or_404(TimeSlotBooking, uuid=booking_uuid)
    except ValidationError as e:
        return HttpResponseBadRequest(e)

    if request.method == "POST":
        base = TimeSlot(added_by=request.user.normaluser, master=booking_obj)
        form = TimeSlotForm(request.POST, instance=base)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(booking_obj.url())

    else:
        form = TimeSlotForm()

    return context_render(request, 'time_booking/book-time.html',
                          context={"booking": booking_obj,
                                   "title": f"Booking | {booking_obj.name}",
                                   "add_timeslot_form": form,
                                   "timeslots": booking_obj.timeslot_set.all()},
                                    )

def add_selected_time_slot(request, booking_uuid):
    f"""
    :param request: With "time_slot_id", "user_string"
    :param booking_uuid: 
    :return: 
    """
    if request.method != "POST":
        return HttpResponseForbidden("Only POST allowed")
    try:
        booking_obj = get_object_or_404(TimeSlotBooking, uuid=booking_uuid)
    except ValidationError as e:

        return HttpResponseBadRequest(e)

    data = json.loads(request.body)

    time_slot_id = data.get("time_slot_id", None)
    print(data)
    if time_slot_id is None:
        return HttpResponseBadRequest("No time slot selected")
    try:
        time_slot = booking_obj.timeslot_set.get(id=int(time_slot_id))
    except TimeSlot.DoesNotExist:
        return HttpResponseBadRequest("Timeslot does not exist or id was not int")
    if request.user.is_authenticated:
        time_slot.add_accepted_by(request.user.normaluser, data.get("user_string", ""))
    else:
        time_slot.add_accepted_by_anon(data.get("user_string", ""))
    return HttpResponse(status=200)

def index(request):
    users_time_slots = TimeSlotBooking.objects.filter(owner=request.user.normaluser).all()\
        if request.user.is_authenticated else []
    print(users_time_slots)
    if request.method == "POST" and request.user.is_authenticated:
        base = TimeSlotBooking(owner=request.user.normaluser)
        form = TimeSlotBookingForm(request.POST, instance=base)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('booking_index'))

    else:
        form = TimeSlotBookingForm()

    return context_render(request, 'time_booking/select-view.html',
                          context={"title": "Time booking",
                                   "add_booking_form": form,
                                   "timeslots": users_time_slots}
                          )
