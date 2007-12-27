#-*- coding: utf-8 -*-
from datetime import date, datetime
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH
from seishinkan.website.models import AUSRICHTUNGEN, Bild

class NewsManager( models.Manager ):
    def get_query_set( self ):
        heute = date.today()
        return super( NewsManager, self ).get_query_set().filter(
            Q( public = True ),
            Q( beginn__lte = heute ) | Q( beginn__isnull = True ),
            Q( ende__gt = heute ) | Q( ende__isnull = True ),
            )

class News( models.Model ):
    title = models.CharField( _( u'Überschrift' ), max_length = DEFAULT_MAX_LENGTH )
    einleitung = models.TextField( _( u'Einleitung' ), blank = True )
    text = models.TextField( _( u'Text' ) )
    bild = models.ForeignKey( Bild, verbose_name = u'Bild', blank = True, null = True )
    bild_ausrichtung = models.CharField( _( u'Bild Ausrichtung' ), max_length = DEFAULT_MAX_LENGTH, choices = AUSRICHTUNGEN, default = u'right', blank = True )
    autor = models.CharField( _( u'Autor' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    beginn = models.DateField( _( u'Veröffentlichung Beginn' ), default = date.today() )
    ende = models.DateField( _( u'Veröffentlichung Ende' ), blank = True, null = True )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = NewsManager()

    def datum( self ):
        if self.beginn:
            return self.beginn
        else:
            return self.creation
    datum.short_description = _( u'Datum' )
    datum.allow_tags = True

    def neu( self ):
        delta = date.today() - self.beginn
        if delta.days < 14 :
            return True
        else:
            return False
    neu.short_description = _( u'Neu' )
    neu.allow_tags = True

    def __unicode__( self ):
        return u'%s'.strip() % ( self.title )

    class Meta:
        ordering = ['-beginn', '-creation', 'title']
        verbose_name = _( u'Beitrag' )
        verbose_name_plural = _( u'Beiträge' )

    class Admin:
        ordering = ['-beginn', '-creation', 'title']
        list_display = ( 'title', 'beginn', 'ende', 'bild', 'creation', 'modified', 'public', 'id' )
        list_filter = ( 'beginn', )
