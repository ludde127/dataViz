import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render

from dataViz.settings import BASE_CONTEXT
from .models import UsersFlashcards, NotePage, FlashCardGroupReference
from .models import filter_non_viewable
from users.models import User

def get_notepage_or_404(request, id):
    try:
        page = filter_non_viewable(request.user, NotePage.objects).get(id__exact=id)
        assert page
        return False, page
    except NotePage.DoesNotExist:
        # User is not allowed to visit this page (and thus its flashcards)...
        return True, HttpResponseNotFound()

def toggle_subscription(request, subscribe=True):
    if request.GET and request.user.is_authenticated:
        # http://127.0.0.1:8000/api-v2/change/subscribe/?page=11&flashcards=47b3d79e-189a-4bd8-99b1-45e2d75106f9
        page = request.GET.get("page")
        flashcard_group = request.GET.get("flashcards")

        err404, page_or_404 = get_notepage_or_404(request, page)
        if err404:
            return page_or_404
        users_flashcards,created_new = UsersFlashcards.objects.get_or_create(user=request.user)
        flashcards,created_new = users_flashcards.flashcard_groups.get_or_create(notepage_id=page, flashcards_id=flashcard_group)

        if flashcards.subscription != subscribe: # False and True per example
            flashcards.subscription = not flashcards.subscription
        users_flashcards.flashcard_groups.add(flashcards)
        flashcards.save()

        users_flashcards.save()

        return HttpResponse("Subscribed", status=200)

    elif not request.user.is_authenticated:
        return HttpResponseForbidden(status=500)

    else:
        return HttpResponseNotFound()
def subscribe_to_flashcard_group(request):
    return toggle_subscription(request, True)

def unsubscribe_to_flashcard_group(request):
    return toggle_subscription(request, False)

def add_flashcard_interactions(request):
    if request.GET and request.user.is_authenticated:
        #http://127.0.0.1:8000/api-v2/change/flashcard-interaction/?page=11&flashcards=47b3d79e-189a-4bd8-99b1-45e2d75106f9&flashcard=fadcd3c1-4520-4a06-8c2d-538d794e9aaf&score=1
        page = request.GET.get("page")
        flashcard_group = request.GET.get("flashcards")
        flashcard = request.GET.get("flashcard")
        score = request.GET.get("score")
        # No longer check the score values, user could fuck up their own algo if they want
        print(score)

        err404, page_or_404 = get_notepage_or_404(request, page)
        if err404:
            return page_or_404
        users_flashcards = UsersFlashcards.objects.get_or_create(user=request.user)[0]
        flashcards: FlashCardGroupReference = users_flashcards.flashcard_groups.get_or_create(
            notepage_id= page, flashcards_id=flashcard_group)[0]
        histories = flashcards.flashcard_histories.get_or_create(user= request.user, flashcard_id =flashcard)[0]

        histories = histories.increment(float(score))

        json_data = {"id": histories.flashcard_id, "score": histories.score,
                     "times_displayed": histories.times_shown, "weight": histories.weight(),
                     "last_displayed_float": histories.last_shown.timestamp()}

        return JsonResponse(data=json_data, status=200)
    return HttpResponseForbidden()

@login_required
def view_flashcards_info(request):
    try:
        users_flashcards = UsersFlashcards.objects.get(user=request.user)
    except UsersFlashcards.DoesNotExist:
        return HttpResponseNotFound("You have no flashcards")
    context = BASE_CONTEXT.copy()
    data = users_flashcards.get_subscribed_flashcards(request, True)
    context["flashcards"] = data
    return render(request, "study_notes/flashcard_info.html", context=context)

@login_required
def user_profile(request, user):
    if user_object := User.objects.get_or_create(username__exact=user)[0]:
        context = BASE_CONTEXT.copy()
        context["are_there_cards"] = False
        context["users_page"] = user
        context["title"] = str(user) + "'s profile"
        try:
            flash_card_list = user_object.usersflashcards.\
                get_subscribed_flashcards(request)
            try:
                context["flash_card_list"] = flash_card_list
                first = flash_card_list[random.randint(0, len(flash_card_list)-1)]
                context["first_card_q"] = first["q"]

                copy = first.copy()
                copy["a"] = str(copy["a"])
                print(copy)
                context["first_card"] = first
                context["amount_of_cards"] = len(flash_card_list)
                context["are_there_cards"] = True

            except (IndexError, ValueError): # value error from the randint if no cards are present.
                pass
        except UsersFlashcards.DoesNotExist:
            pass
        return render(request, "study_notes/user_profile.html", context=context)
    return HttpResponseNotFound()