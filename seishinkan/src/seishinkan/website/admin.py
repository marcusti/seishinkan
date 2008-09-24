#-*- coding: utf-8 -*-

from django.contrib import admin
from seishinkan.website.models import *

class WochentagAdmin( admin.ModelAdmin ):
    ordering = ['index', 'name']
    list_display = ( 'name', 'public', 'creation', 'modified', 'index' )

class DokumentAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'datei', 'modified', 'id' )

class OrtAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'modified', 'id' )

class BildAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'bild', 'max_breit', 'max_hoch', 'modified', 'admin_thumb' )
    list_display_links = ( 'name', 'admin_thumb' )
    search_fields = [ 'name', 'bild' ]

class SeiteAdmin( admin.ModelAdmin ):
    prepopulated_fields = {'url': ( 'name', )}
    ordering = ['name']
    search_fields = [ 'name' ]
    list_display = ( 'name', 'url', 'parent', 'position', 'is_homepage', 'public', 'id' )
    list_filter = ( 'parent', )

class ArtikelAdmin( admin.ModelAdmin ):
    ordering = ['position', 'title', 'text']
    search_fields = [ 'title', 'text' ]
    list_display = ( 'get_title', 'preview', 'seite', 'position', 'public', 'id' )
    list_display_links = ( 'get_title', 'preview' )
    list_filter = ( 'seite', )
    fieldsets = (
        ( None, { 'fields': ( 'seite', 'position', 'public' ) } ),
        ( 'Bild', { 'fields': ( 'bild', 'bild_ausrichtung' ) } ),
        ( 'HTML Code', { 'fields': ( 'text_src', ) } ),
        ( 'Deutsch', { 'fields': ( 'title', 'text' ) } ),
        ( 'Englisch', { 'fields': ( 'title_en', 'text_en' ), 'classes': ( 'collapse', ) } ),
        ( 'Japanisch', { 'fields': ( 'title_ja', 'text_ja' ), 'classes': ( 'collapse', ) } ),
    )

    class Media:
        js = ( '/static/js/tiny_mce/tiny_mce.js',
              '/static/js/textareas.js', )

class TerminAdmin( admin.ModelAdmin ):
    ordering = ['-ende', '-beginn', 'title']
    date_hierarchy = 'ende'
    search_fields = [ 'title', 'text', 'ort' ]
    list_display = ( 'title', 'beginn', 'ende', 'bild', 'modified', 'public', 'id' )
    list_filter = ( 'beginn', 'ende', )

    class Media:
        js = ( '/static/js/tiny_mce/tiny_mce.js',
              '/static/js/textareas.js', )

class TrainingsartAdmin( admin.ModelAdmin ):
    ordering = ['name']
    list_display = ( 'name', 'ist_anfaengerkurs', 'ist_kindertraining', 'public', 'id' )
    fieldsets = (
        ( 'Deutsch', { 'fields': ( 'name', 'text', ) } ),
        ( 'Englisch', { 'fields': ( 'name_en', 'text_en' ), 'classes': ( 'collapse', ) } ),
        ( 'Japanisch', { 'fields': ( 'name_ja', 'text_ja' ), 'classes': ( 'collapse', ) } ),
        ( None, { 'fields': ( 'ist_anfaengerkurs', 'ist_kindertraining', 'public' ) } ),
    )

class TrainingAdmin( admin.ModelAdmin ):
    ordering = ['wochentag', 'von']
    list_display = ( 'wochentag', 'von', 'bis', 'art', 'creation', 'modified', 'public' )

class TrainingAktuellAdmin( admin.ModelAdmin ):
    ordering = [ '-ende', '-beginn', 'name' ]
    search_fields = [ 'name', 'text' ]
    list_display = ( 'name', 'text', 'beginn', 'ende', 'public' )
    fieldsets = (
        ( None, { 'fields': ( 'name', 'text', 'beginn', 'ende', 'public' ) } ),
        ( 'Englisch', { 'fields': ( 'text_en', ), 'classes': ( 'collapse', ) } ),
        ( 'Japanisch', { 'fields': ( 'text_ja', ), 'classes': ( 'collapse', ) } ),
    )

class DownloadAdmin( admin.ModelAdmin ):
    ordering = [ '-modified' ]
    search_fields = [ 'name', 'text', 'datei' ]
    list_display = ( 'name', 'datei', 'modified', 'public' )

class KontaktAdmin( admin.ModelAdmin ):
    ordering = [ '-creation' ]
    search_fields = [ 'sender', 'betreff', 'nachricht' ]
    list_display = ( 'sender', 'betreff', 'kurzform', 'creation' )
    list_display_links = ( 'sender', 'betreff', 'kurzform' )

admin.site.register( Ort, OrtAdmin )
admin.site.register( Dokument, DokumentAdmin )
admin.site.register( Kontakt, KontaktAdmin )
admin.site.register( Download, DownloadAdmin )
admin.site.register( TrainingAktuell, TrainingAktuellAdmin )
admin.site.register( Training, TrainingAdmin )
admin.site.register( Trainingsart, TrainingsartAdmin )
admin.site.register( Termin, TerminAdmin )
admin.site.register( Artikel, ArtikelAdmin )
admin.site.register( Seite, SeiteAdmin )
admin.site.register( Bild, BildAdmin )
admin.site.register( TitelBild, BildAdmin )
admin.site.register( Wochentag, WochentagAdmin )
