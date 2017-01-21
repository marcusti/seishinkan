#-*- coding: utf-8 -*-

from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH

class LinkKategorieManager( models.Manager ):
    def get_query_set( self ):
        return super( LinkKategorieManager, self ).get_query_set().filter( public = True )

class LinkManager( models.Manager ):
    def get_query_set( self ):
        return super( LinkManager, self ).get_query_set().filter( public = True )

class LinkKategorie( models.Model ):
    name = models.CharField( max_length = DEFAULT_MAX_LENGTH, unique = True )
    position = models.IntegerField( _( u'Position auf der Seite' ), default = 0, blank = True )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = LinkKategorieManager()

    def __unicode__( self ):
        return u'%s' % ( self.name )

    class Meta:
        ordering = [ 'position', 'name' ]
        verbose_name = _( u'Link-Kategorie' )
        verbose_name_plural = _( u'Link-Kategorien' )

class LinkKategorieAdmin( admin.ModelAdmin ):
    ordering = [ 'position', 'name' ]
    list_display = ( 'name', 'position', 'public', 'modified' )
    list_display_links = ( 'name', )

admin.site.register( LinkKategorie, LinkKategorieAdmin )

class Link( models.Model ):
    url = models.URLField( verify_exists = False, unique = True )
    title = models.CharField( max_length = DEFAULT_MAX_LENGTH )
    text = models.TextField( _( u'Text' ), blank = True )
    position = models.IntegerField( _( u'Position auf der Seite' ), default = 0, blank = True )
    kategorie = models.ForeignKey( LinkKategorie, verbose_name = _( 'Kategorie' ) )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = LinkManager()

    def __unicode__( self ):
        return u'%s' % ( self.title )

#    def get_absolute_url( self ):
#        return '/links/'

    class Meta:
        ordering = [ 'position', 'title' ]
        verbose_name = _( u'Link' )
        verbose_name_plural = _( u'Links' )

class LinkAdmin( admin.ModelAdmin ):
    ordering = [ 'title' ]
    list_display = ( 'title', 'url', 'kategorie', 'position', 'public' )
    list_display_links = ( 'title', 'url' )
    list_filter = ( 'kategorie', )

admin.site.register( Link, LinkAdmin )
