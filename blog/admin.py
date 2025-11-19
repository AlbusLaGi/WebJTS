from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'tipo_contenido', 'fecha_publicacion', 'esta_publicado')
    list_filter = ('tipo_contenido', 'fecha_publicacion', 'esta_publicado')
    search_fields = ('titulo', 'descripcion_breve', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
    ordering = ('-fecha_publicacion',)
    filter_horizontal = ()
