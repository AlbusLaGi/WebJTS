from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import Product, Package

def product_list(request):
    # Redirigir a la vista categorizada para mantener consistencia
    return categorized_product_list(request)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)

    # Obtener productos relacionados (mismos de la misma categoría) en orden aleatorio
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(slug=slug).order_by('?')[:4]

    # Obtener información de autores si está presente
    authors_info = ""
    if product.authors:
        # Si hay información de autores
        authors_info = product.authors
    else:
        authors_info = ""

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'additional_info': authors_info
    })

def package_detail(request, slug):
    package = get_object_or_404(Package, slug=slug, is_available=True)
    return render(request, 'products/package_detail.html', {'package': package})

def categorized_product_list(request):
    """Vista para mostrar productos organizados por categorías"""
    # Obtener productos por categorías específicas
    products = Product.objects.filter(is_available=True)

    # Obtener el filtro de categoría si existe
    category_filter = request.GET.get('category', None)

    if category_filter and category_filter != 'all':
        # Filtrar por categoría específica y ordenar aleatoriamente
        categorias = {}
        categorias[category_filter] = products.filter(category=category_filter).order_by('?')
    else:
        # Mostrar todas las categorías con productos ordenados aleatoriamente
        categorias = {}
        for cat_choice, cat_name in Product.CATEGORIA_CHOICES:
            categorias[cat_choice] = products.filter(category=cat_choice).order_by('?')

    # Diccionario para traducir las categorías al plural para mostrar en la web
    categoria_plurales = {
        'paquete': 'Paquetes',
        'serie': 'Series',
        'libro': 'Libros',
        'otro_producto': 'Otros Productos'
    }

    context = {
        'categorias': categorias,
        'categoria_choices': dict(Product.CATEGORIA_CHOICES),
        'categoria_plurales': categoria_plurales,
        'current_category': category_filter
    }
    return render(request, 'products/categorized_product_list.html', context)

# Importar la funcionalidad de importación desde Google Sheets
from .google_sheet_importer import import_products_with_gspread

@staff_member_required
@require_POST
def import_products_from_sheet(request):
    """
    Vista para importar productos desde una URL de Google Sheets
    """
    sheet_url = request.POST.get('sheet_url', '').strip()

    if not sheet_url:
        messages.error(request, 'La URL del Google Sheet es requerida.')
        return redirect('admin:products_product_changelist')

    try:
        imported_count, errors = import_products_with_gspread(sheet_url, delete_existing=True)

        if imported_count > 0:
            messages.success(request, f'Se importaron {imported_count} productos exitosamente.')

        if errors:
            for error in errors:
                messages.error(request, f'Error: {error}')

    except Exception as e:
        messages.error(request, f'Error al importar el archivo: {str(e)}')

    return redirect('admin:products_product_changelist')