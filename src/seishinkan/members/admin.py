#-*- coding: utf-8 -*-

from django.contrib import admin
from seishinkan.members.models import *

class LandAdmin( admin.ModelAdmin ):
    ordering = ['name']
    list_display = ( 'name', 'id' )

class GraduierungAdmin( admin.ModelAdmin ):
    ordering = ['-graduierung', '-datum', 'person']
    list_display = ( 'person', 'datum', 'graduierung', 'vorschlag', 'public', 'modified', 'id' )
    list_filter = ( 'vorschlag', 'graduierung', 'person' )
    search_fields = ( 'person__vorname', 'person__nachname' )

class GraduierungInline( admin.TabularInline ):
    model = Graduierung
    extra = 1

class MitgliedAdmin( admin.ModelAdmin ):
    ordering = ['id']
    list_display = ( 'id', 'vorname', 'nachname', 'aktuelle_graduierung', 'status', 'email', 'alter', 'mitglied_seit' )
    list_display_links = ( 'vorname', 'nachname' )
    list_filter = ( 'status', 'land', 'ist_vorstand', 'ist_trainer', 'ist_kind', 'mitglied_seit')
    list_per_page = 200
    search_fields = ( 'vorname', 'nachname', 'email', 'text' )
    inlines = [ GraduierungInline, ]

admin.site.register( Mitglied, MitgliedAdmin )
admin.site.register( Graduierung, GraduierungAdmin )
admin.site.register( Land, LandAdmin )
