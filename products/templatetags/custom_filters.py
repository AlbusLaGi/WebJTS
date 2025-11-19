from django import template
from django.utils.text import Truncator
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Obtiene un item de un diccionario usando una clave
    """
    return dictionary.get(key)

@register.filter
def truncate_description(text, max_lines=3):
    """
    Trunca una descripción a un número máximo de líneas o caracteres,
    terminando con '...' y un enlace 'leer más'.
    """
    if not text:
        return ""

    # Dividir el texto en líneas
    lines = text.split('\n')

    # Tomar solo el número máximo de líneas
    truncated_lines = lines[:max_lines]
    truncated_text = '\n'.join(truncated_lines)

    # Contar solo las palabras de las primeras líneas para truncar
    words = truncated_text.split()

    # Limitar a 30 palabras para mantenerlo corto
    if len(words) > 30:
        truncated_text = ' '.join(words[:30]) + '...'

    return truncated_text