from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from tags.models import Tag


class BlogPost(models.Model):
    """
    Modelo para entradas de blog que pueden contener contenido multimedia,
    lecturas, reflexiones, audios, etc.
    """
    TIPO_CONTENIDO_CHOICES = [
        ('LECTURA', 'Lectura'),
        ('REFLEXION', 'Reflexión'),
        ('AUDIO', 'Audio'),
        ('VIDEO', 'Video'),
        ('ARTICULO', 'Artículo'),
        ('DEVOCIONAL', 'Devocional'),
        ('OTRO', 'Otro'),
    ]

    titulo = models.CharField(max_length=255, verbose_name="Título")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL Slug")
    contenido = models.TextField(verbose_name="Contenido", blank=True, null=True)
    tipo_contenido = models.CharField(
        max_length=20,
        choices=TIPO_CONTENIDO_CHOICES,
        default='ARTICULO',
        verbose_name="Tipo de Contenido"
    )
    fecha_publicacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Publicación")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="blog_posts", verbose_name="Autor")

    # Campos para contenido multimedia
    imagen_destacada = models.ImageField(upload_to='blog/imagenes/', null=True, blank=True, verbose_name="Imagen Destacada")
    archivo_audio = models.FileField(upload_to='blog/audios/', null=True, blank=True, verbose_name="Archivo de Audio")
    archivo_video = models.FileField(upload_to='blog/videos/', null=True, blank=True, verbose_name="Archivo de Video")
    enlace_multimedia = models.URLField(blank=True, null=True, verbose_name="Enlace a Contenido Multimedia")

    # Metadatos
    descripcion_breve = models.TextField(max_length=500, blank=True, verbose_name="Descripción Breve")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Etiquetas")
    es_destacado = models.BooleanField(default=False, verbose_name="Destacado")
    esta_publicado = models.BooleanField(default=True, verbose_name="Publicado")

    class Meta:
        verbose_name = "Entrada de Blog"
        verbose_name_plural = "Entradas de Blog"
        ordering = ['-fecha_publicacion']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('blog:detalle_post', kwargs={'slug': self.slug})
