#-*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH

class LinkManager( models.Manager ):
    def get_query_set( self ):
        return super( LinkManager, self ).get_query_set().filter( public = True )

class LinkKategorie( models.Model ):
    name = models.CharField( max_length = DEFAULT_MAX_LENGTH, unique = True )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    def __unicode__( self ):
        return u'%s' % ( self.name )

    class Meta:
        ordering =[ 'name' ]
        verbose_name = _( u'Link-Kategorie' )
        verbose_name_plural = _( u'Link-Kategorien' )

    class Admin:
        ordering =[ 'name' ]
        list_display = ( 'name', )
        list_display_links = ( 'name', )

class Link( models.Model ):
    url = models.URLField( verify_exists = False, unique = True )
    title = models.CharField( max_length = DEFAULT_MAX_LENGTH )
    text = models.TextField( _( u'Text'), blank = True )
    position = models.IntegerField( _( u'Position auf der Seite' ), default = 0, blank = True )
    kategorie = models.ForeignKey( LinkKategorie, verbose_name = _( 'Kategorie' ) )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = LinkManager()

    def __unicode__( self ):
        return u'%s' % ( self.title )

    def get_absolute_url( self ):
        return '/links/'

    class Meta:
        ordering = [ 'title' ]
        verbose_name = _( u'Link' )
        verbose_name_plural = _( u'Links' )

    class Admin:
        ordering = [ 'title' ]
        list_display = ( 'title', 'url', 'position' )
        list_display_links = ( 'title', 'url' )
        list_filter = ( 'kategorie', )
