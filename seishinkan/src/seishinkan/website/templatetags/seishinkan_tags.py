from datetime import date
from django import template
from django.template.defaultfilters import stringfilter
import os

register = template.Library()

@register.filter
@stringfilter
def fromtimestamp( value ):
    try:
        return date.fromtimestamp( int( value ) )
    except:
        return value

@register.filter
@stringfilter
def extension( value ):
    try:
        root, ext =  os.path.splitext( value )
        if ext and len( ext ) > 0:
            if ext.startswith( '.' ):
                return ext.lower()[1:]
            else:
                return ext.lower()
        return value
    except:
        return value
