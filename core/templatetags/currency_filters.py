from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
import math

register = template.Library()

@register.filter
def format_currency(value):
    if value is None or value == '':
        return ""
    try:
        # Asegurarse de que el valor sea un Decimal antes de formatear
        from decimal import Decimal
        value = Decimal(value)
        # Formatear el número con separador de miles y sin decimales, luego reemplazar la coma por un punto
        formatted_value = "{:,.0f}".format(value).replace(",", ".")
        return "COP$" + formatted_value
    except (ValueError, TypeError, Decimal.InvalidOperation):
        return ""

@register.filter
def get_discounted_price(price, discount_percent=15):
    """
    Retorna el precio incrementado (con 15% o 20%) redondeado al número entero más cercano
    Por ejemplo: si el precio es 13000, con 15% sería 14950, que se redondea a 15000
    """
    try:
        from decimal import Decimal
        price = float(price)
        if discount_percent not in [15, 20]:
            discount_percent = 15  # Valor por defecto

        increased_price = price * (1 + discount_percent/100)

        # Redondear al número entero más cercano
        increased_price = round(increased_price)

        # Si el número es mayor a 1000, redondear a la centena más cercana para simplificar
        if increased_price > 1000:
            increased_price = round(increased_price, -2)  # Redondear a centenas

        return increased_price
    except (ValueError, TypeError):
        return 0
