#-*- coding: utf-8 -*-

from django.contrib import admin
from seishinkan.members.models import *

class PersonAdmin( admin.ModelAdmin ):
    ordering = ['firstname', 'lastname']
    list_display = ( 'firstname', 'lastname', 'public', 'modified', 'id' )
    list_display_links = ( 'firstname', 'lastname' )

admin.site.register( Person, PersonAdmin )
