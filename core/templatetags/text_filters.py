

import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='bold_biblical_quotes')
def bold_biblical_quotes(value):
    """
    Finds text matching the pattern "Biblical quote" (Citation X:Y)
    and wraps it in <b> tags.
    """
    # Regex to find a string in double quotes followed by a space and a citation in parentheses
    # Example: "Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar." (Mt 11:28)
    pattern = r'(".*?"\s*\\(.*?\\))'
    
    def make_bold(match):
        return f'<b>{match.group(1)}</b>'

    # Use re.sub with a function to replace all occurrences
    bolded_text = re.sub(pattern, make_bold, value)
    
    return mark_safe(bolded_text)

