#-*- coding: utf-8 -*-

from django.contrib import admin
from seishinkan.members.models import *

class GraduierungAdmin( admin.ModelAdmin ):
    ordering = ['-graduierung', '-datum', 'person']
    list_display = ( 'person', 'datum', 'graduierung', 'public', 'modified', 'id' )
    list_filter = ( 'graduierung', 'person' )
    search_fields = ( 'person__vorname', 'person__nachname' )

class GraduierungInline( admin.TabularInline ):
    model = Graduierung
    extra = 1

class MitgliedAdmin( admin.ModelAdmin ):
    ordering = ['id']
    list_display = ( 'id', 'vorname', 'nachname', 'aktuelle_graduierung', 'status', 'email', 'alter', 'modified' )
    list_display_links = ( 'vorname', 'nachname' )
    list_filter = ( 'status', 'ist_vorstand', 'ist_trainer', 'ist_kind')
    list_per_page = 200
    search_fields = ( 'vorname', 'nachname', 'email', 'text' )
    inlines = [ GraduierungInline, ]

admin.site.register( Mitglied, MitgliedAdmin )
admin.site.register( Graduierung, GraduierungAdmin )
