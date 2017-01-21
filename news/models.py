#-*- coding: utf-8 -*-

from datetime import date, datetime
from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH, AbstractModel
from seishinkan.website.models import AUSRICHTUNGEN, Bild
from seishinkan.members.models import Mitglied

class NewsManager( models.Manager ):
    def get_query_set( self ):
        heute = date.today()
        return super( NewsManager, self ).get_query_set().filter(
            Q( public = True ),
            Q( beginn__lte = heute ) | Q( beginn__isnull = True ),
            Q( ende__gt = heute ) | Q( ende__isnull = True ),
            )

class News( AbstractModel ):
    title = models.CharField( _( u'Überschrift' ), max_length = DEFAULT_MAX_LENGTH )
    einleitung = models.TextField( _( u'Einleitung' ), blank = True )
    text = models.TextField( _( u'Text' ) )
    bild = models.ForeignKey( Bild, verbose_name = u'Bild', blank = True, null = True )
    bild_ausrichtung = models.CharField( _( u'Bild Ausrichtung' ), max_length = DEFAULT_MAX_LENGTH, choices = AUSRICHTUNGEN, default = u'right', blank = True )
    beginn = models.DateField( _( u'veröffentlicht' ), default = date.today() )
    ende = models.DateField( _( u'endet' ), blank = True, null = True )
    autoren = models.ManyToManyField( Mitglied, verbose_name = 'Autoren', blank = True, null = True )

    objects = models.Manager()
    public_objects = NewsManager()

    def datum( self ):
        if self.beginn:
            return self.beginn
        else:
            return self.creation
    datum.short_description = _( u'Datum' )
    datum.allow_tags = True

    text.allow_tags = True

    def neu( self ):
        return ( date.today() - self.beginn ).days < 14
    neu.short_description = _( u'Neu' )
    neu.allow_tags = False

    def get_absolute_url( self ):
        return '/news/%s/' % ( self.id )

    def __unicode__( self ):
        return u'%s'.strip() % ( self.title )

    def preview( self ):
        idx = 100
        text = self.text.strip()
        if len( text ) <= idx:
            return text
        else:
            return '%s [...]' % ( text[:idx] )
    preview.short_description = _( u'Vorschau' )
    preview.allow_tags = False

    class Meta:
        ordering = ['-beginn', '-creation', 'title']
        verbose_name = _( u'Beitrag' )
        verbose_name_plural = _( u'Beiträge' )
