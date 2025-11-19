from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    """
    A generic tag that can be associated with any other model in the project,
    such as Events, Products, and Media Items.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name