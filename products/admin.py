from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product, Package

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'authors': forms.TextInput(attrs={'placeholder': 'Ingresa los autores, separados por comas', 'maxlength': 500}),
        }
        labels = {
            'authors': 'Autores',
        }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'category', 'get_authors', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description', 'category', 'authors')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description', 'image', 'price', 'is_available')
        }),
        ('Categorización', {
            'fields': ('category',)
        }),
        ('Detalles del Producto', {
            'fields': ('pages', 'measures', 'authors'),
            'description': 'Campos opcionales'
        }),
        ('Etiquetas', {
            'fields': ('tags',)
        }),
    )

    def get_authors(self, obj):
        """Muestra los autores en la lista de productos"""
        if obj.authors:
            return obj.authors[:50] + '...' if len(obj.authors) > 50 else obj.authors
        return '-'
    get_authors.short_description = 'Autores'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Agregar el botón de importación de Google Sheets
        extra_context['show_google_sheet_import'] = True
        extra_context['import_url'] = reverse('products:import_products_from_sheet')
        extra_context['title'] = 'Productos'
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'created_at')
    list_filter = ('is_available',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('products', 'tags')
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'slug', 'description', 'image', 'price', 'is_available')
        }),
        ('Productos Incluidos', {
            'fields': ('products',),
            'description': 'Selecciona los productos que incluye este paquete.'
        }),
        ('Etiquetas', {
            'fields': ('tags',)
        }),
    )