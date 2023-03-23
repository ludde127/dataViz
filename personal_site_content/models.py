from django.db import models

# Create your models here.

class Page(models.Model):
    page_title = models.CharField(max_length=60, verbose_name="Title name of the webpage")

    @classmethod
    def get_index_page_pk(cls):
        page, created = cls.objects.get_or_create(page_title="Index")
        return page.pk

class TextSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, default=Page.get_index_page_pk)

    title = models.CharField(max_length=100, verbose_name="Title of block")
    text = models.TextField("Text to display")

    image = models.FileField("A image to add to the content", null=True, blank=True) # File field as image does not suppport webp
    image_alt = models.CharField(max_length=150, blank=True)
    weight = models.IntegerField("A higher number will put the item higher up on the personal site.")

    def __str__(self):
        return self.title
