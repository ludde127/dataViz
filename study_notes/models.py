from wagtail.fields import RichTextField, StreamField
from django import forms
from wagtail.blocks import RichTextBlock, CharBlock, StructBlock, IntegerBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailcodeblock.blocks import CodeBlock
from wagtailmath.blocks import MathBlock # Have to do this weird fix https://github.com/JamesRamm/wagtailmath/issues/7

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from django.db import models
from wagtail.search import index

import users.models
from dataViz.settings import BASE_CONTEXT
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

import json
from wagtail.models import Page, Orderable, PageViewRestriction

from wagtail_home.models import filter_non_viewable


# https://docs.wagtail.org/en/v4.1.1/getting_started/tutorial.html

class QuizCard(StructBlock):
    question = CharBlock(required=True)
    answer = CharBlock(required=True)
    score = IntegerBlock(required=False)

class FlashCard(StructBlock):
    question = CharBlock(required=True)

class ManyQuizCards(StructBlock):
    title = CharBlock(max_length=200, required=False)
    cards = StreamBlock([("Card", QuizCard()), ], use_json_field=True)
    passing_score = IntegerBlock(required=False)

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

        user = request.user
        pages = self.get_children().live()

        # Unauthenticated users can only see public pages
        if not user.is_authenticated:
            pages = pages.public()
        # Superusers can implicitly view all pages. No further filtering required
        elif not user.is_superuser:
            # Get all page ids where the user's groups do NOT have access to
            disallowed_ids = PageViewRestriction.objects.exclude(groups__id=user.groups.all()).values_list("NotePage",
                                                                                                           flat=True)
            # Exclude all pages with disallowed ids
            pages = pages.exclude(id__in=disallowed_ids)


        context['note_pages'] = pages.order_by('-first_published_at')
        return context


class NotePage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    #body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=NotePageTag, blank=True)
    categories = ParentalManyToManyField('study_notes.NoteCategory', blank=True)
    subpage_types = []
    parent_page_type = ["study_notes.NotesIndexPage"]
    body = StreamField([
        ('heading', CharBlock(form_classname="title")),
        ('paragraph', RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('code', CodeBlock(label="Code")),
        ('equation', MathBlock()),
        ("quiz", ManyQuizCards()),
        ("flashcards", ManyFlashcards())
    ], use_json_field=True)


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

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context.update(BASE_CONTEXT)
        quiz_json = {}
        quiz_start = {}
        quiz_length = {}
        for (i, b) in enumerate(self.body.blocks_by_name("quiz")):
            block = b.value
            print(block)
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



        flashcards_json = {}
        flashcards_start = {}
        flashcards_length = {}
        for (i, b) in enumerate(self.body.blocks_by_name("flashcards")):
            block = b.value
            print(block)
            inner = {"title": block["title"]}
            flashcards = {}
            first_question = ""
            for (j, card) in enumerate(block["cards"]):
                if not first_question:
                    first_question = card.value["question"]
                flashcards[str(j)] = {"q": card.value["question"]}
            inner["cards"] = flashcards

            flashcards_json[b.id] = inner
            flashcards_start[b.id] = first_question
            flashcards_length[b.id] = len(block["cards"])

        quiz_json.update(flashcards_json)
        quiz_start.update(flashcards_start)
        quiz_length.update(flashcards_length)
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

from wagtail.snippets.models import register_snippet


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


