#-*- coding: utf-8 -*-

from django.contrib import admin
from seishinkan.members.models import *

class PersonAdmin( admin.ModelAdmin ):
    ordering = ['vorname', 'nachname']
    list_display = ( 'vorname', 'nachname', 'public', 'modified', 'id' )
    list_display_links = ( 'vorname', 'nachname' )

class GraduierungInline( admin.TabularInline ):
    model = Graduierung

class MitgliedAdmin( admin.ModelAdmin ):
    ordering = ['vorname', 'nachname']
    list_display = ( 'vorname', 'nachname', 'status', 'public', 'modified', 'id' )
    list_display_links = ( 'vorname', 'nachname' )
    inlines = [ GraduierungInline, ]

admin.site.register( Person, PersonAdmin )
admin.site.register( Mitglied, MitgliedAdmin )

