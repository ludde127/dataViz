import datetime

from wagtail import hooks
from wagtail.api import APIField
from wagtail.fields import RichTextField, StreamField
from django import forms
from wagtail.blocks import RichTextBlock, CharBlock, StructBlock, IntegerBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailcodeblock.blocks import CodeBlock
from wagtailmath.blocks import MathBlock # Have to do this weird fix https://github.com/JamesRamm/wagtailmath/issues/7

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from django.db import models
from wagtail.search import index
from wagtail.snippets.models import register_snippet

import users.models
from dataViz.settings import BASE_CONTEXT
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

import json
from wagtail.models import Page, Orderable

from wagtail_home.models import filter_non_viewable


# https://docs.wagtail.org/en/v4.1.1/getting_started/tutorial.html

@register_snippet
class FlashCardHistory(models.Model):
    user = models.ForeignKey(to="users.User",on_delete=models.CASCADE, default=None)
    flashcard_id = models.UUIDField("Id of flashcard")
    last_shown = models.DateTimeField("Last shown to user", auto_now=True, editable=False)
    times_shown = models.IntegerField("Amount of times shown to user", default=0)
    score = models.FloatField("The score", default=0)

    class Meta:
        unique_together = ["user", "flashcard_id"]
    def increment(self, score_change=0, save=True):
        self.score += score_change
        self.times_shown += 1
        if save:
            self.save()

    def weight(self):
        return -self.score

@register_snippet
class FlashCardGroupReference(models.Model):
    notepage_id = models.IntegerField() # Id of the notepage the flashcards are in
    flashcards_id = models.UUIDField("Id of the flashcard group")
    subscription = models.BooleanField(default=False)
    flashcard_histories = models.ManyToManyField(FlashCardHistory)


class QuizCard(StructBlock):
    question = CharBlock(required=True)
    answer = CharBlock(required=True)
    score = IntegerBlock(required=False)

class ManyQuizCards(StructBlock):
    title = CharBlock(max_length=200, required=False)
    cards = StreamBlock([("Card", QuizCard()), ], use_json_field=True)
    passing_score = IntegerBlock(required=False)

class FlashCard(StructBlock):
    question = CharBlock(required=True, max_length=300)
    answer = CharBlock(required=True)

class ManyFlashcards(StructBlock):
    title = CharBlock(max_length=200, required=False)
    cards = StreamBlock([("Card", FlashCard()), ], use_json_field=True)

class NotePageTag(TaggedItemBase):
    subpage_types = []
    parent_page_type = ["wagtail_home.HomePage"]

    content_object = ParentalKey(
        "NotePage", related_name="tagged_items", on_delete=models.CASCADE
    )

class NotesIndexPage(Page):
    #title = RichTextField(blank=False)
    intro = RichTextField(blank=True)
    subpage_types = ["study_notes.NotePage"]
    parent_page_type = ["wagtail_home.HomePage"]
    content_panels = Page.content_panels + [
        #FieldPanel('titel'),
        FieldPanel('intro')
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context.update(BASE_CONTEXT)

        pages = self.get_children().live()




        context['note_pages'] = filter_non_viewable(request.user, pages.order_by('-first_published_at'), "NotePage")
        return context


class NotePage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    #body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=NotePageTag, blank=True)
    categories = ParentalManyToManyField('study_notes.NoteCategory', blank=True)
    subpage_types = ["study_notes.NotePage",]
    parent_page_type = ["study_notes.NotesIndexPage",]
    body = StreamField([
        ('heading', CharBlock(form_classname="title")),
        ('richtext', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('code', CodeBlock(label="Code")),
        ('equation', MathBlock()),
        ("quiz", ManyQuizCards()),
        ("flashcards", ManyFlashcards())
    ], use_json_field=True, collapsed=True)

    api_fields = [
        APIField("body"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Note information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    def get_quiz(self):
        quiz_json = {}
        quiz_start = {}
        quiz_length = {}
        for (i, b) in enumerate(self.body.blocks_by_name("quiz")):
            block = b.value
            # print(block)
            inner = {"title": block["title"], "passing_score": block["passing_score"]}
            cards = {}
            first_question = ""
            for (j, card) in enumerate(block["cards"]):
                if not first_question:
                    first_question = card.value["question"]
                cards[str(j)] = {"q": card.value["question"], "a": card.value["answer"], "score": card.value["score"]}
            inner["cards"] = cards

            quiz_json[b.id] = inner
            quiz_start[b.id] = first_question
            quiz_length[b.id] = len(block["cards"])
        return quiz_json, quiz_start, quiz_length

    def get_flashcards(self, request):
        flashcards_json = {}
        flashcards_start = {}
        flashcards_length = {}
        subscribed_cards = set()
        for (i, b) in enumerate(self.body.blocks_by_name("flashcards")):
            block = b.value
            try:
                # This could be used later.
                reference = request.user.usersflashcards.flashcard_groups.get(flashcards_id=b.id, notepage_id=self.id, subscription=True)
            except (UsersFlashcards.DoesNotExist, FlashCardGroupReference.DoesNotExist):
                pass
            else:
                subscribed_cards.add(b.id)

            # print(block)
            inner = {"title": block["title"]}
            flashcards = {}
            first_question = ""
            for (j, card) in enumerate(block["cards"]):
                if not first_question:
                    first_question = card.value["question"]
                flashcards[str(j)] = {"q": card.value["question"], "a": card.value["answer"], "id": card.id}
            inner["cards"] = flashcards

            flashcards_json[b.id] = inner
            flashcards_start[b.id] = first_question
            flashcards_length[b.id] = len(block["cards"])
        return flashcards_json, flashcards_start, flashcards_length, list(subscribed_cards)


    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context.update(BASE_CONTEXT)


        quiz_json, quiz_start, quiz_length = self.get_quiz()
        flashcards_json, flashcards_start, flashcards_length, subscribed_cards = self.get_flashcards(request)
        context["page_id"] = self.id
        context["subscribed_cards"] = subscribed_cards
        context["flash_json"] = flashcards_json
        context["flash_starts"] = flashcards_start
        context["flash_lengths"] = flashcards_length

        context["quiz_json"] = quiz_json
        context["quiz_starts"] = quiz_start
        context["quiz_lengths"] = quiz_length
        return context

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

class NotePageGalleryImage(Orderable):
    subpage_types = []
    parent_page_type = ["study_notes.NotePage"]
    page = ParentalKey(NotePage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


class NoteTagIndexPage(Page):
    subpage_types = []
    parent_page_type = ["wagtail_home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)

        # Filter by tag

        tag = request.GET.get('tag')
        if tag:
            pages = NotePage.objects.live().filter(tags__name=tag)

            context['notepages'] = filter_non_viewable(request.user, pages, "NotePage")

        # Update template context
        context.update(BASE_CONTEXT)

        return context



@register_snippet
class NoteCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Note categories'


@register_snippet
class UsersFlashcards(models.Model):
    flashcard_groups = models.ManyToManyField(FlashCardGroupReference)
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)

    def get_subscribed_flashcards(self, request):

        """Create a flat list of all the cards.

        class FlashCardHistory(models.Model):
            user = models.ForeignKey(to="users.User",on_delete=models.CASCADE, default=None)
            flashcard_id = models.UUIDField("Id of flashcard")
            last_shown = models.DateTimeField("Last shown to user", auto_now=True, editable=False)
            times_shown = models.IntegerField("Amount of times shown to user", default=0)
            score = models.FloatField("The score", default=0)
        """
        flashcard_list = list()
        subscribed = [l for l in self.flashcard_groups.filter(subscription=True)]

        notepages = set([l.notepage_id for l in subscribed])

        flashcard_blocks_to_get_per_notepage: dict[str, set[str]] = dict()
        for n_id in notepages:
            flashcard_blocks_to_get_per_notepage[n_id] = set([str(l.flashcards_id) for l in subscribed if l.notepage_id == n_id])

        for notepage_id in notepages:
            to_render = [e for e in NotePage.objects.get(id__exact=notepage_id).body.blocks_by_name("flashcards")
                         if str(e.id) in flashcard_blocks_to_get_per_notepage[notepage_id]]

            print("RENDER LEN", len(to_render))
            for b in to_render:
                block = b.value
                string_block_id = str(b.id)
                # print(block)
                for card in block["cards"]:
                    times_displayed = 0
                    score = 0
                    weight = 0
                    try:
                        history = FlashCardHistory.objects.get(user=request.user, flashcard_id__exact=card.id)
                        score = history.score
                        times_displayed = history.score
                        weight = history.weight()
                    except FlashCardHistory.DoesNotExist:
                        print("Does not exist")

                    flashcard_list.append({"q": card.value["question"], "a": card.value["answer"],
                                          "id": card.id, "block_id": string_block_id, "notepage_id": notepage_id,
                                           "score": score, "times_displayed": times_displayed, "weight": weight})

        print(flashcard_list)
        return flashcard_list


def get_notepage_from_id(request, id):
    resp = filter_non_viewable(request.user, NotePage.objects, "NotePage")
    try:
        return resp.get(id__exact=id)
    except NotePage.DoesNotExist:
        return None