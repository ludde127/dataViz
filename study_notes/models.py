import json
import time

from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.blocks import RichTextBlock, CharBlock, StructBlock, IntegerBlock, StreamBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.templatetags.wagtailcore_tags import richtext
from wagtailcodeblock.blocks import CodeBlock

from dataViz.settings import BASE_CONTEXT
from wagtail_home.customizations.widgets.math_jax import MathBlock
from wagtail_home.models import filter_non_viewable


# https://docs.wagtail.org/en/v4.1.1/getting_started/tutorial.html

@register_snippet
class FlashCardHistory(models.Model):
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE, default=None)
    flashcard_id = models.UUIDField("Id of flashcard")
    last_shown = models.DateTimeField("Last shown to user", auto_now=True, editable=False)
    times_shown = models.IntegerField("Amount of times shown to user", default=0)
    score = models.FloatField("The score", default=0)

    time_score_array = ArrayField(ArrayField(models.FloatField(), size=2, null=True),
                                  null=True)  # This is ment to store [(interaction_time, score), ...]

    class Meta:
        unique_together = ["user", "flashcard_id"]

    def increment(self, score_change=0, save=True):
        self.score += score_change
        self.times_shown += 1

        array = self.time_score_array
        if array is None:
            array = list()

        t = time.time()
        array.append([t, score_change])

        self.time_score_array = array
        if save:
            self.save()
        return self

    def get_array(self) -> list:
        array = self.time_score_array
        if array is None:
            array = list()
        return array

    def weight(self):
        array = self.get_array()
        val = 1e8  # No data stored so far. This will weigh heavily
        if len(array) > 3:
            val = -sum((e[1] for e in array[-3:])) / 3
        elif len(array) > 0:
            val = -sum((e[1] for e in array)) / len(array)
        else:
            return val

        return val
        # return -60*val - self.last_shown.timestamp()
        # return -self.score/self.times_shown


@register_snippet
class FlashCardGroupReference(models.Model):
    notepage_id = models.IntegerField()  # Id of the notepage the flashcards are in
    flashcards_id = models.UUIDField("Id of the flashcard group")
    subscription = models.BooleanField(default=False)
    flashcard_histories = models.ManyToManyField(FlashCardHistory)

    def to_dict(self):
        dict_repr = {}
        dict_repr["notepage_id"] = self.notepage_id

        dict_repr["flashcards_id"] = self.flashcards_id

        histories = list()
        dict_repr["histories"] = histories


def get_flashcard_history(card, user):
    times_displayed = 0
    score = 0
    weight = 0
    last_displayed_float = 0
    try:
        if user.is_authenticated:
            history = FlashCardHistory.objects.get(user=user, flashcard_id__exact=card.id)
            score = history.score
            times_displayed = history.times_shown
            weight = history.weight()
            last_displayed_float = history.last_shown.timestamp()
    except FlashCardHistory.DoesNotExist:
        print("Flashcard history does not exist")
    return {"last_displayed_float": last_displayed_float,
            "score": score,
            "times_displayed": times_displayed,
            "weight": weight}


class QuizCard(StructBlock):
    question = CharBlock(required=True)
    answer = CharBlock(required=True)
    score = IntegerBlock(required=False)


class ManyQuizCards(StructBlock):
    title = CharBlock(max_length=200, required=False)
    cards = StreamBlock([("Card", QuizCard()), ], use_json_field=True)
    passing_score = IntegerBlock(required=False)


class FlashCard(StructBlock):
    question = RichTextBlock(required=True, max_length=600)
    answer = RichTextBlock(required=True, max_length=5000)


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
    # title = RichTextField(blank=False)
    intro = RichTextField(blank=True)
    subpage_types = ["study_notes.NotePage"]
    parent_page_type = ["wagtail_home.HomePage"]
    content_panels = Page.content_panels + [
        # FieldPanel('titel'),
        FieldPanel('intro')
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context.update(BASE_CONTEXT)

        pages = self.get_children().live()

        context['title'] = "All Notes"

        context['note_pages'] = filter_non_viewable(request.user, pages.order_by('-first_published_at'))
        return context


class NotePage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250, blank=True)
    # body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=NotePageTag, blank=True)
    categories = ParentalManyToManyField('study_notes.NoteCategory', blank=True)
    subpage_types = ["study_notes.NotePage", ]
    parent_page_type = ["study_notes.NotesIndexPage", ]

    views = models.BigIntegerField(default=0, editable=False)

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
        index.AutocompleteField('intro'),
        index.AutocompleteField('body'),
        index.RelatedFields('tags', [
            index.AutocompleteField('name'),
        ]),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Note information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images")
    ]

    @staticmethod
    def get_flashcard_blocks(page_id, block_ids):
        return [e for e in NotePage.objects.get(id__exact=page_id).body.blocks_by_name("flashcards")
                if str(e.id) in block_ids]

    def get_quiz(self):
        quiz_json = {}
        quiz_start = {}
        quiz_length = {}
        for b in self.body.blocks_by_name("quiz"):
            block = b.value
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

    @property
    def default_seo_search_description(self):
        return f"{self.title.capitalize()}. {self.intro}"

    @property
    def meta_description(self):
        return self.search_description if self.search_description else self.default_seo_search_description

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_flashcards(self, request):
        flashcards_json = {}
        flashcards_length = {}
        for b in self.body.blocks_by_name("flashcards"):
            block = b.value

            inner = {
                "title": block["title"],
                "is_subscribed": False
            }

            try:
                if request.user.is_authenticated:
                    reference = request.user.usersflashcards.flashcard_groups.get(flashcards_id=b.id,
                                                                                  notepage_id=self.id,
                                                                                  subscription=True)
            except (UsersFlashcards.DoesNotExist, FlashCardGroupReference.DoesNotExist):
                pass
            else:
                inner["is_subscribed"] = True

            flashcards = [{
                "q": str(richtext(card.value["question"])),
                "a": str(richtext(card.value["answer"])),
                "id": card.id,
                "block_id": str(b.id),
                "notepage_id": self.id,
                **get_flashcard_history(card, request.user)
            } for card in block["cards"]]

            inner["cards"] = json.dumps(flashcards)

            flashcards_json[b.id] = inner
            flashcards_length[b.id] = len(block["cards"])
        return flashcards_json, flashcards_length

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context.update(BASE_CONTEXT)

        quiz_json, quiz_start, quiz_length = self.get_quiz()
        flashcards_json, flashcards_length = self.get_flashcards(request)
        context["page_id"] = self.id
        context["flash_json"] = flashcards_json
        context["flash_lengths"] = flashcards_length

        context["quiz_json"] = quiz_json
        context["quiz_starts"] = quiz_start
        context["quiz_lengths"] = quiz_length
        context["title"] = self.title

        context["live_revision"] = {
            "user": self.live_revision.user,
            "created_at": self.live_revision.created_at,
        }

        self.views += 1
        self.save()
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

            context['notepages'] = filter_non_viewable(request.user, pages)
        context["title"] = "Tag: " + tag
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
        if request.user.is_authenticated:
            return self.get_users_flashcards(request.user)
        return []

    def get_users_flashcards(self, user):
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
            flashcard_blocks_to_get_per_notepage[n_id] = set(
                [str(l.flashcards_id) for l in subscribed if l.notepage_id == n_id])

        for notepage_id in notepages:
            to_render = NotePage.get_flashcard_blocks(notepage_id, flashcard_blocks_to_get_per_notepage[notepage_id])

            for b in to_render:
                block = b.value
                string_block_id = str(b.id)
                for card in block["cards"]:
                    entry = {"q": str(richtext(card.value["question"])),
                             "a": str(richtext(card.value["answer"])),
                             "id": card.id,
                             "block_id": string_block_id,
                             "notepage_id": notepage_id,
                             **get_flashcard_history(card, user)}
                    flashcard_list.append(entry)

        return flashcard_list


def get_notepage_from_id(request, id):
    resp = filter_non_viewable(request.user, NotePage.objects)
    try:
        return resp.get(id__exact=id)
    except NotePage.DoesNotExist:
        return None
