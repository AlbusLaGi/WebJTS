from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tags.models import Tag

class Product(models.Model):
    # Categorías integradas directamente como opciones
    CATEGORIA_CHOICES = [
        ('paquete', 'Paquete'),
        ('serie', 'Serie'),
        ('libro', 'Libro'),
        ('otro_producto', 'Otro Producto'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagen")

    # Categoría integrada como lista desplegable
    category = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name="Categoría")

    # Campos comunes para todos los productos
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    # Campos específicos (algunos aplican a ciertos tipos de productos)
    pages = models.IntegerField(blank=True, null=True, verbose_name="Páginas")
    measures = models.CharField(max_length=100, blank=True, null=True, verbose_name="Medidas (ej. 15x20 cm)")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Etiquetas")

    # Información de autores del producto
    authors = models.TextField(blank=True, null=True, verbose_name="Autores")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

class Package(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del Paquete")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")
    image = models.ImageField(upload_to='packages/', blank=True, null=True, verbose_name="Imagen del Paquete")
    products = models.ManyToManyField(Product, blank=True, verbose_name="Productos Incluidos")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Etiquetas")

    class Meta:
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:package_detail', kwargs={'slug': self.slug})