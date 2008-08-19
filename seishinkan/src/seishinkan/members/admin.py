#-*- coding: utf-8 -*-

from django.contrib import admin
from seishinkan.members.models import *

class PersonAdmin( admin.ModelAdmin ):
    ordering = ['vorname', 'nachname']
    list_display = ( 'vorname', 'nachname', 'public', 'modified', 'id' )
    list_display_links = ( 'vorname', 'nachname' )
    list_per_page = 200
    search_fields = ( 'vorname', 'nachname', 'email', 'text' )

class GraduierungAdmin( admin.ModelAdmin ):
    ordering = ['id']
    list_display = ( 'person', 'datum', 'graduierung', 'public', 'modified', 'id' )

class GraduierungInline( admin.TabularInline ):
    model = Graduierung

class MitgliedAdmin( admin.ModelAdmin ):
    ordering = ['id']
    list_display = ( 'id', 'vorname', 'nachname', 'aktuelle_graduierung', 'status', 'email', 'geburt', 'mitglied_seit', 'ist_vorstand', 'ist_trainer', 'ist_kind' )
    list_display_links = ( 'vorname', 'nachname' )
    list_filter = ( 'status', 'ist_vorstand', 'ist_trainer', 'ist_kind')
    list_per_page = 200
    search_fields = ( 'vorname', 'nachname', 'email', 'text' )
    inlines = [ GraduierungInline, ]

admin.site.register( Person, PersonAdmin )
admin.site.register( Mitglied, MitgliedAdmin )
admin.site.register( Graduierung, GraduierungAdmin )

