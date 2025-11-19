from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import BlogPost


def blog_list(request):
    """
    Vista para listar todas las entradas de blog
    """
    posts = BlogPost.objects.filter(esta_publicado=True).order_by('-fecha_publicacion')
    
    # Paginación
    paginator = Paginator(posts, 10)  # 10 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'titulo_pagina': 'Blog - Jesús Te Sana'
    }
    return render(request, 'blog/blog_list.html', context)


def blog_detalle(request, slug):
    """
    Vista para mostrar un post específico del blog
    """
    post = get_object_or_404(BlogPost, slug=slug, esta_publicado=True)
    
    # Obtener posts relacionados (mismo tipo o mismas etiquetas)
    posts_relacionados = BlogPost.objects.filter(
        tipo_contenido=post.tipo_contenido, 
        esta_publicado=True
    ).exclude(slug=slug)[:3]
    
    context = {
        'post': post,
        'posts_relacionados': posts_relacionados,
        'titulo_pagina': f'{post.titulo} - Blog Jesús Te Sana'
    }
    return render(request, 'blog/blog_detalle.html', context)


def blog_por_tipo(request, tipo_contenido):
    """
    Vista para listar entradas de blog por tipo de contenido
    """
    posts = BlogPost.objects.filter(
        tipo_contenido=tipo_contenido.upper(), 
        esta_publicado=True
    ).order_by('-fecha_publicacion')
    
    # Paginación
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener el nombre amigable del tipo de contenido
    tipo_nombres = {
        'LECTURA': 'Lecturas',
        'REFLEXION': 'Reflexiones',
        'AUDIO': 'Audios',
        'VIDEO': 'Videos',
        'ARTICULO': 'Artículos',
        'DEVOCIONAL': 'Devocionales',
        'OTRO': 'Otros Contenidos'
    }
    titulo_tipo = tipo_nombres.get(tipo_contenido.upper(), tipo_contenido)
    
    context = {
        'page_obj': page_obj,
        'titulo_tipo': titulo_tipo,
        'titulo_pagina': f'{titulo_tipo} - Jesús Te Sana'
    }
    return render(request, 'blog/blog_por_tipo.html', context)