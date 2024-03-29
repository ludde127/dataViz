import json

import django.db.utils
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from dataViz.settings import BASE_CONTEXT
from dataViz.utils import context_render
from users.models import User
from .models import UsersFlashcards, NotePage, FlashCardGroupReference
from .models import filter_non_viewable


def get_notepage_or_404(request, id):
    try:
        page = filter_non_viewable(
            request.user, NotePage.objects).get(id__exact=id)
        assert page
        return False, page
    except NotePage.DoesNotExist:
        # User is not allowed to visit this page (and thus its flashcards)...
        return True, HttpResponseNotFound()


def toggle_subscription(request, subscribe=True):
    if request.user.is_authenticated:
        _json = json.loads(request.body)
        # http://127.0.0.1:8000/api-v2/change/subscribe/?page=11&flashcards=47b3d79e-189a-4bd8-99b1-45e2d75106f9
        page = _json.get("page")
        flashcard_group = _json.get("flashcards")

        err404, page_or_404 = get_notepage_or_404(request, page)
        if err404:
            return page_or_404
        users_flashcards, created_new = UsersFlashcards.objects.get_or_create(user=request.user)
        flashcards, created_new = users_flashcards.flashcard_groups.get_or_create(notepage_id=page,
                                                                                  flashcards_id=flashcard_group)

        if flashcards.subscription != subscribe:  # False and True per example
            flashcards.subscription = not flashcards.subscription
        users_flashcards.flashcard_groups.add(flashcards)
        flashcards.save()

        users_flashcards.save()

        return HttpResponse("Updated subscription", status=200)

    elif not request.user.is_authenticated:
        return HttpResponseForbidden(status=500)

    else:
        return HttpResponseNotFound()


@require_POST
@csrf_exempt
@login_required
def subscribe_to_flashcard_group(request):
    return toggle_subscription(request, True)


@require_POST
@csrf_exempt
@login_required
def unsubscribe_to_flashcard_group(request):
    return toggle_subscription(request, False)


@require_POST
@csrf_exempt
@login_required
def add_flashcard_interactions(request):
    _json = json.loads(request.body)
    # http://127.0.0.1:8000/api-v2/change/flashcard-interaction/?page=11&flashcards=47b3d79e-189a-4bd8-99b1-45e2d75106f9&flashcard=fadcd3c1-4520-4a06-8c2d-538d794e9aaf&score=1
    page = _json.get("page")
    flashcard_group = _json.get("flashcards")
    flashcard = _json.get("flashcard")
    score = _json.get("score")

    err404, page_or_404 = get_notepage_or_404(request, page)
    if err404:
        return page_or_404
    users_flashcards = UsersFlashcards.objects.get_or_create(user=request.user)[0]
    flashcards: FlashCardGroupReference = users_flashcards.flashcard_groups.get_or_create(
        notepage_id=page,
        flashcards_id=flashcard_group)[0]
    histories = flashcards.flashcard_histories.get_or_create(
        user=request.user,
        flashcard_id=flashcard)[0]

    histories = histories.increment(float(score))

    json_data = {"id": histories.flashcard_id, "score": histories.score,
                 "times_displayed": histories.times_shown, "weight": histories.weight(),
                 "last_displayed_float": histories.last_shown.timestamp()}

    return JsonResponse(data=json_data, status=200)


@login_required
def view_flashcards_info(request):
    try:
        users_flashcards = UsersFlashcards.objects.get(user=request.user)
    except UsersFlashcards.DoesNotExist:
        return HttpResponseNotFound("You have no flashcards")
    context = BASE_CONTEXT.copy()
    data = users_flashcards.get_subscribed_flashcards(request, True)
    context["flashcards"] = data
    return context_render(request, "study_notes/flashcard_info.html", context=context)


@login_required
def user_profile(request, user):
    try:
        user_object = User.objects.get_or_create(username__exact=user)[0]
    except django.db.utils.IntegrityError:
        user_object = None

    if user_object:
        context = BASE_CONTEXT.copy()
        context["current_user_id"] = request.user.id
        context["are_there_cards"] = False
        context["users_page"] = user_object
        context["users_id"] = user_object.id
        context["title"] = str(user) + "'s profile"
        try:
            flash_card_list = user_object.usersflashcards.get_subscribed_flashcards(request)
            if flash_card_list and len(flash_card_list) > 0:
                context["flash_card_list"] = json.dumps(flash_card_list)
                context["amount_of_cards"] = len(flash_card_list)
                context["are_there_cards"] = True
        except UsersFlashcards.DoesNotExist:
            pass
        return context_render(request, "study_notes/user_profile.html", context=context)
    return HttpResponseNotFound()
