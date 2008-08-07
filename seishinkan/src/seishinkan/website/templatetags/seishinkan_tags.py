from datetime import date
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def fromtimestamp( value ):
    try:
        return date.fromtimestamp( int( value ) )
    except:
        return value
