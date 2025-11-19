from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from tags.models import Tag


# Modelo para los Cuori (Corazones) - Base de datos central de personas
class Cuori(models.Model):
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo")
    cedula = models.CharField(max_length=20, verbose_name="Cédula", unique=True)
    numero_contacto = models.CharField(max_length=20, verbose_name="Número de Contacto 1")
    numero_contacto_2 = models.CharField(max_length=20, verbose_name="Número de Contacto 2", blank=True, null=True)
    email_contacto = models.EmailField(verbose_name="Correo Electrónico")
    pais = models.CharField(max_length=100, verbose_name="País", null=True, blank=True)
    departamento = models.CharField(max_length=100, verbose_name="Departamento/Estado/Región", null=True, blank=True)
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad", null=True, blank=True)

    def __str__(self):
        return self.nombre_completo

    class Meta:
        verbose_name = "Cuori"
        verbose_name_plural = "Cuoris"
        ordering = ['nombre_completo']

# Modelo para los Eventos (Retiros, Conferencias, etc.)
class Evento(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha = models.DateTimeField(verbose_name="Fecha y Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin", null=True, blank=True)
    lugar = models.CharField(max_length=255, verbose_name="Lugar")
    direccion = models.CharField(max_length=255, verbose_name="Dirección", blank=True)
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad", default='Bogotá D.C')
    departamento = models.CharField(max_length=100, verbose_name="Departamento", default='Cundinamarca')
    ASISTENCIA_CHOICES = [
        ('LIMITADO', 'Cupos Limitados'),
        ('ABIERTO', 'Ilimitado'),
    ]
    PUBLICO_CHOICES = [
        ('TODOS', 'Para todos'),
        ('MUJERES', 'Solo mujeres'),
        ('HOMBRES', 'Solo hombres'),
        ('PAREJAS', 'Parejas'),
        ('INFANTES', 'Infantes'),
    ]

    cupos = models.PositiveIntegerField(default=0, verbose_name="Cupos")
    tipo_asistencia = models.CharField(max_length=10, choices=ASISTENCIA_CHOICES, default='LIMITADO', verbose_name="Tipo de Asistencia")
    dirigido_a = models.CharField(max_length=10, choices=PUBLICO_CHOICES, default='TODOS', verbose_name="Dirigido a")
    coordenadas_mapa = models.CharField(max_length=100, blank=True, verbose_name="Coordenadas de Mapa (Latitud, Longitud)")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL Slug")
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True, verbose_name="Imagen Promocional")
    requiere_ofrenda = models.BooleanField(default=False, verbose_name="¿Requiere Ofrenda?")
    valor_ofrenda = models.IntegerField(null=True, blank=True, verbose_name="Valor de la Ofrenda en COP$")
    requiere_inscripcion = models.BooleanField(default=True, verbose_name="¿Requiere Inscripción?")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Etiquetas")

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    @property
    def cupos_disponibles(self):
        return self.cupos - self.inscritos.count()

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['fecha']

# Modelo para las Inscripciones a los eventos
class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="inscritos")
    cuori = models.ForeignKey(Cuori, on_delete=models.CASCADE, related_name="inscripciones")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Inscripción", null=True, blank=True)

    def __str__(self):
        return f"{self.cuori.nombre_completo} inscrito en {self.evento.titulo}"

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        unique_together = ('evento', 'cuori')
