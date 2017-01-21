#-*- coding: utf-8 -*-

from django.contrib import admin
from seishinkan.news.models import *

class NewsAdmin( admin.ModelAdmin ):
    ordering = ['-beginn', '-creation', 'title']
    date_hierarchy = 'beginn'
    search_fields = [ 'title', 'einleitung', 'text' ]
    list_display = ( 'title', 'preview', 'beginn', 'ende', 'bild', 'public', 'id' )
    list_display_links = ( 'title', 'preview' )
    list_filter = ( 'beginn', 'autoren' )
    filter_horizontal = ( 'autoren', )
    js = ['tiny_mce/tiny_mce.js', 'js/textareas.js']

    class Media:
        js = ( '/static/js/tiny_mce/tiny_mce.js',
              '/static/js/textareas.js', )

admin.site.register( News, NewsAdmin )
