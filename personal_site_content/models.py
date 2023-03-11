from django.db import models

# Create your models here.

class TextSection(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title of block")
    text = models.TextField("Text to display")

    image = models.ImageField("A image to add to the content", null=True)

    weight = models.IntegerField("A higher number will put the item higher up on the personal site.")

    def __str__(self):
        return self.title