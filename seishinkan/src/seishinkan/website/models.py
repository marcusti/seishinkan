#-*- coding: utf-8 -*-

from datetime import date, datetime
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH
import os

AUSRICHTUNGEN = [
    ( u'left', u'links' ),
    ( u'right', u'rechts' ),
]

class Wochentag( models.Model ):
    name = models.CharField( _( u'Name' ), max_length = DEFAULT_MAX_LENGTH )
    name_en = models.CharField( _( u'Name (Englisch)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    name_ja = models.CharField( _( u'Name (Japanisch)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    index = models.IntegerField( _( u'Index (Reihenfolge)' ), default = 0 )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    def get_name( self, language = None ):
        return getattr( self, "name_%s" % ( language or translation.get_language()[:2] ), "" ) or self.name

    def __unicode__( self ):
        return u'%s'.strip() % ( self.get_name() )

    class Meta:
        ordering = ['index', 'name']
        verbose_name = _( u'Wochentag' )
        verbose_name_plural = _( u'Wochentage' )

class Dokument( models.Model ):
    name = models.CharField( _( u'Titel' ), max_length = DEFAULT_MAX_LENGTH, help_text = u'' )
    datei = models.FileField( _( u'Datei' ), upload_to = 'dokumente/' )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    def __unicode__( self ):
        return u'%s (%s)' % ( self.name, self.datei )

    class Meta:
        ordering = ['name']
        verbose_name = _( u'Dokument' )
        verbose_name_plural = _( u'Dokumente' )

class Ort( models.Model ):
    name = models.CharField( _( u'Titel' ), max_length = DEFAULT_MAX_LENGTH, help_text = u'' )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _( u'Ort' )
        verbose_name_plural = _( u'Orte' )

class BildManager( models.Manager ):
    def get_query_set( self ):
        return super( BildManager, self ).get_query_set().filter( public = True )

class Bild( models.Model ):
    name = models.CharField( _( u'Titel' ), max_length = DEFAULT_MAX_LENGTH, unique = True, help_text = u'Der Name muss eindeutig sein.' )
    bild = models.ImageField( _( u'Datei' ), upload_to = 'bilder/' )
    vorschau = models.ImageField( _( u'Vorschau' ), upload_to = 'bilder/thumbs/', blank = True, editable = False )
    max_breit = models.IntegerField( _( u'max. Breite' ), default = 200, help_text = u'Das Bild wird automatisch auf die angegebene Breite skaliert. (Das Seitenverhältnis bleibt erhalten.)' )
    max_hoch = models.IntegerField( _( u'max. Höhe' ), default = 200, help_text = u'Das Bild wird automatisch auf die angegebene Höhe skaliert. (Das Seitenverhältnis bleibt erhalten.)' )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = BildManager()

    def save( self ):
        if self.bild:
            if not self.name or self.name.strip() == '':
                self.name = self.bildpath
            from PIL import Image
            THUMBNAIL_SIZE = ( 75, 75 )
            SCALE_SIZE = ( self.max_breit, self.max_hoch )
            if not self.vorschau:
                self.vorschau.save( self.bild.path, '' )
            image = Image.open( self.bild.path )
            image.thumbnail( SCALE_SIZE, Image.ANTIALIAS )
            image.save( self.bild.path )
            if image.mode not in ( 'L', 'RGB' ):
                image = image.convert( 'RGB' )
            image.thumbnail( THUMBNAIL_SIZE, Image.ANTIALIAS )
            image.save( self.vorschau.path )
            super( Bild, self ).save()

    def admin_thumb( self ):
        w = self.vorschau.width
        h = self.vorschau.height
        return u'<img src="%s" width="%s" height="%s" />' % ( self.vorschau.url, w, h )
    admin_thumb.short_description = _( u'Bild' )
    admin_thumb.allow_tags = True

    def __unicode__( self ):
        return '%s (%s %s)' % ( self.name, self.bild, self.modified )

    class Meta:
        ordering = ['name']
        verbose_name = _( u'Bild' )
        verbose_name_plural = _( u'Bilder' )

class TitelBild( Bild ):
    
    class Meta:
        ordering = ['name']
        verbose_name = _( u'Bild im Kopf' )
        verbose_name_plural = _( u'Bilder im Kopf' )

class SeitenManager( models.Manager ):
    def get_query_set( self ):
        return super( SeitenManager, self ).get_query_set().filter( public = True )

    def get_homepage( self ):
        homepage = None
        for hp in self.get_query_set().filter( is_homepage = True ):
            homepage = hp
        return homepage

class Seite( models.Model ):
    name = models.CharField( _( u'Name' ), max_length = DEFAULT_MAX_LENGTH )
    name_en = models.CharField( _( u'Name (Englisch)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    name_ja = models.CharField( _( u'Name (Japanisch)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    url = models.SlugField( _( u'URL' ), unique = True, max_length = DEFAULT_MAX_LENGTH )
    position = models.IntegerField( _( u'Position im Menü' ), default = 0 )
    parent = models.ForeignKey( 'self', verbose_name = _( u'Über' ), null = True, blank = True, related_name = 'child_set' )
    titelbild = models.ForeignKey( TitelBild, verbose_name = u'Bild im Kopf', blank = True, null = True )
    show_events = models.BooleanField( _( u'Enthält Termine Übersicht' ), default = False )
    show_news = models.BooleanField( _( u'Enthält Beiträge Übersicht' ), default = False )
    show_training = models.BooleanField( _( u'Enthält Trainingszeiten' ), default = False )
    show_anfaenger = models.BooleanField( _( u'Enthält Anfängerkurs Info' ), default = False )
    show_kinder = models.BooleanField( _( u'Enthält Kindertraining Info' ), default = False )
    is_homepage = models.BooleanField( _( u'Ist Startseite' ), default = False, editable = False )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = SeitenManager()

    def get_titelbild( self ):
        if self.titelbild:
            return self.titelbild

        if self.parent and self.parent.titelbild:
            return self.parent.titelbild

        return None
    
    def get_sub_sites( self ):
        return self.child_set.filter( public = True ).order_by( 'position', 'name' )

    def has_sub_sites( self ):
        return self.child_set.filter( public = True ).count() > 0

    def get_name( self, language = None ):
        return getattr( self, "name_%s" % ( language or translation.get_language()[:2] ), "" ) or self.name

    def __unicode__( self ):
        return u'%s'.strip() % ( self.name )

    def get_absolute_url( self ):
        return '/%s/' % self.url

    class Meta:
        ordering = ['name']
        verbose_name = _( u'Seite' )
        verbose_name_plural = _( u'Seiten' )

class ArtikelManager( models.Manager ):
    def get_query_set( self ):
        return super( ArtikelManager, self ).get_query_set().filter( public = True )

    def get_by_category( self, kid ):
        return self.get_query_set().filter( seite = kid ).order_by( 'position' )

class Artikel( models.Model ):
    title = models.CharField( _( u'Überschrift' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    title_en = models.CharField( _( u'Überschrift' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    title_ja = models.CharField( _( u'Überschrift' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    text = models.TextField( _( u'Text' ), blank = True )
    text_en = models.TextField( _( u'Text' ), blank = True )
    text_ja = models.TextField( _( u'Text' ), blank = True )
    text_src = models.CharField( _( u'Code' ), max_length = 5000, blank = True, help_text = u'Wird für einige Seiten benötigt, die Scripte enthalten. Z.B. bei der Google Map im Lageplan. Den Code bitte nicht im Editor Fenster von TinyMCE eingeben.' )
    position = models.IntegerField( _( u'Position auf der Seite' ), default = 0, blank = True )
    bild = models.ForeignKey( Bild, verbose_name = u'Bild', blank = True, null = True )
    bild_ausrichtung = models.CharField( _( u'Bild Ausrichtung' ), max_length = DEFAULT_MAX_LENGTH, choices = AUSRICHTUNGEN, default = u'right', blank = True )
    seite = models.ForeignKey( Seite, verbose_name = _( u'Seite' ) )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = ArtikelManager()

    def get_title( self, language = None ):
        return getattr( self, "title_%s" % ( language or translation.get_language()[:2] ), "" ) or self.title
    get_title.short_description = _( u'Überschrift' )
    get_title.allow_tags = False

    def get_text( self, language = None ):
        return getattr( self, "text_%s" % ( language or translation.get_language()[:2] ), "" ) or self.text
    get_text.short_description = _( u'Text' )
    get_text.allow_tags = False

    def get_absolute_url( self ):
        return '/seite/%i/' % self.seite.id

    def __unicode__( self ):
        if self.get_title().strip() == '':
            return self.preview()
        return u'%s'.strip() % ( self.title )

    def preview( self ):
        idx = 100
        text = self.get_text().strip()
        if len( text ) <= idx:
            return text
        else:
            return u'%s [...]' % ( text[:idx] )
    preview.short_description = _( u'Vorschau' )
    preview.allow_tags = False

    class Meta:
        ordering = ['position', 'title', 'text']
        verbose_name = _( u'Artikel' )
        verbose_name_plural = _( u'Artikel' )

class TerminManager( models.Manager ):
    def get_query_set( self ):
        return super( TerminManager, self ).get_query_set().filter( public = True ).order_by( '-ende', '-beginn', 'title' )

    def current( self ):
        heute = date.today()
        return self.get_query_set().filter( Q( beginn__gte = heute ) | Q( ende__gte = heute ) ).order_by( 'ende', 'beginn', 'title' )

class Termin( models.Model ):
    title = models.CharField( _( u'Überschrift' ), max_length = DEFAULT_MAX_LENGTH )
    text = models.TextField( _( u'Text' ) )
    ort = models.ForeignKey( Ort, blank = True, null = True )
    bild = models.ForeignKey( Bild, verbose_name = u'Bild', blank = True, null = True )
    bild_ausrichtung = models.CharField( _( u'Bild Ausrichtung' ), max_length = DEFAULT_MAX_LENGTH, choices = AUSRICHTUNGEN, default = u'right', blank = True )
    dokument = models.ForeignKey( Dokument, blank = True, null = True )
    beginn = models.DateField( _( u'Beginn' ) )
    ende = models.DateField( _( u'Ende' ) )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = TerminManager()

    def ist_heute( self ):
        heute = date.today()
        return self.beginn <= heute and self.ende >= heute
    
    def get_absolute_url( self ):
        return '/termin/%i/' % self.id

    def __unicode__( self ):
        return u'%s'.strip() % ( self.title )

    class Meta:
        ordering = ['-ende', '-beginn', 'title']
        verbose_name = _( u'Termin' )
        verbose_name_plural = _( u'Termine' )

class TrainingManager( models.Manager ):
    def get_einheit( self, tag, anfang ):
        return Training.objects.get( public = True, wochentag = tag, von = anfang )

    def get_einheiten_pro_tag( self, tag ):
        return Training.objects.filter( public = True, wochentag = tag )

    def get_anfangs_zeiten( self ):
        return Training.objects.filter( public = True ).values( 'von' ).order_by( 'von' ).distinct()

    def get_wochentage( self ):
        return Wochentag.objects.filter( training__isnull = False, public = True ).distinct()

    def get_wochenplan( self ):
        plan = []
        for zeit in self.get_anfangs_zeiten():
            row = []
            for tag in self.get_wochentage():
                try:
                    row.append( self.get_einheit( tag, zeit['von'] ) )
                except:
                    row.append( None )
            plan.append( row )
        return plan

class Trainingsart( models.Model ):
    name = models.CharField( _( u'Name' ), max_length = DEFAULT_MAX_LENGTH )
    name_en = models.CharField( _( u'Name (Englisch)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    name_ja = models.CharField( _( u'Name (Japanisch)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    text = models.TextField( _( u'Text' ), blank = True )
    text_en = models.TextField( _( u'Text (Englisch)' ), blank = True )
    text_ja = models.TextField( _( u'Text (Japanisch)' ), blank = True )
    ist_anfaengerkurs = models.BooleanField( _( u'Anfängerkurs' ), default = False )
    ist_kindertraining = models.BooleanField( _( u'Kindertraining' ), default = False )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    def get_name( self, language = None ):
        return getattr( self, "name_%s" % ( language or translation.get_language()[:2] ), "" ) or self.name

    def get_text( self, language = None ):
        return getattr( self, "text_%s" % ( language or translation.get_language()[:2] ), "" ) or self.text

    def __unicode__( self ):
        return u'%s'.strip() % ( self.get_name() )

    class Meta:
        ordering = ['name']
        verbose_name = _( u'Trainingsart' )
        verbose_name_plural = _( u'Trainingsarten' )

class Training( models.Model ):
    '''Modell einer Trainingseinheit'''
    von = models.TimeField( _( u'Von' ) )
    bis = models.TimeField( _( u'Bis' ) )
    art = models.ForeignKey( Trainingsart, verbose_name = _( u'Trainingsart' ) )
    wochentag = models.ForeignKey( Wochentag, verbose_name = _( u'Wochentag' ) )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    def __unicode__( self ):
        return u'%s %s - %s'.strip() % ( self.wochentag, self.von, self.bis )

    class Meta:
        ordering = ['wochentag', 'von']
        verbose_name = _( u'Training' )
        verbose_name_plural = _( u'Training' )

class TrainingAktuellManager( models.Manager ):
    def get_query_set( self ):
        return super( TrainingAktuellManager, self ).get_query_set().filter( public = True )

    def get_aktuelle_meldungen( self ):
        heute = date.today()
        return self.get_query_set().filter( beginn__lte = heute, ende__gte = heute )

class TrainingAktuell( models.Model ):
    name = models.CharField( _( u'Name' ), max_length = DEFAULT_MAX_LENGTH, help_text = u'Der Name dient nur zur Übersicht und wird auf der Webseite nicht angezeigt.' )
    text = models.TextField( _( u'Text' ), help_text = u'Dieser Text wird unter der Rubrik "Training heute" angezeigt.' )
    text_en = models.TextField( _( u'Text (Englisch)' ), blank = True )
    text_ja = models.TextField( _( u'Text (Japanisch)' ), blank = True )
    beginn = models.DateField( _( u'Beginn' ), help_text = u'Ab diesem Datum wird der Text auf der Webseite angezeigt.' )
    ende = models.DateField( _( u'Ende' ), help_text = u'Bis zu diesem Datum (einschließlich) wird der Text auf der Webseite angezeigt.' )
    
    public = models.BooleanField( _( u'Öffentlich' ), default = True, help_text = u'Nur öffentliche Objekte erscheinen auf der Webseite.' )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = TrainingAktuellManager()

    def __unicode__( self ):
        return u'%s'.strip() % ( self.name )

    def get_text( self, language = None ):
        return getattr( self, "text_%s" % ( language or translation.get_language()[:2] ), "" ) or self.text

    def get_absolute_url( self ):
        return '/'

    class Meta:
        ordering = ['-ende', '-beginn', 'name']
        verbose_name = _( u'Training Aktuell Meldung' )
        verbose_name_plural = _( u'Training Aktuell Meldungen' )

class DownloadManager( models.Manager ):
    def get_query_set( self ):
        return super( DownloadManager, self ).get_query_set().filter( public = True )

class Download( models.Model ):
    name = models.CharField( _( u'Name' ), max_length = DEFAULT_MAX_LENGTH )
    text = models.TextField( _( u'Text' ) )
    datei = models.FileField( _( u'Pfad' ), upload_to = 'downloads/' )
    vorschau = models.ImageField( _( u'Vorschau' ), upload_to = 'bilder/thumbs/', blank = True, editable = False )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = DownloadManager()

    def save( self ):
        try:
            if self.datei:
                from PIL import Image
                THUMBNAIL_SIZE = ( 75, 75 )
                if not self.vorschau:
                    self.save_vorschau_file( self.get_datei_filename(), '' )
                image = Image.open( self.get_datei_filename() )
                if image.mode not in ( 'L', 'RGB' ):
                    image = image.convert( 'RGB' )
                image.thumbnail( THUMBNAIL_SIZE, Image.ANTIALIAS )
                image.save( self.get_vorschau_filename() )
        except:
            pass

        super( Download, self ).save()

    def __unicode__( self ):
        return u'%s %s'.strip() % ( self.name, self.datei )

    def get_absolute_url( self ):
        return '/downloads/'

    class Meta:
        ordering = ['-modified']
        verbose_name = _( u'Download' )
        verbose_name_plural = _( u'Downloads' )

class Kontakt( models.Model ):
    sender = models.EmailField( _( u'Absender' ) )
    betreff = models.CharField( _( u'Betreff' ), max_length = DEFAULT_MAX_LENGTH )
    captcha = models.CharField( _( u'Captcha' ), max_length = DEFAULT_MAX_LENGTH )
    nachricht = models.TextField( _( u'Nachricht' ) )
    to = models.TextField( _( u'Empfänger' ) )

    public = models.BooleanField( _( u'Öffentlich' ), default = False )
    creation = models.DateTimeField( _( u'Gesendet am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    def kurzform( self ):
        return self.nachricht[:50]
    kurzform.short_description = _( u'Nachricht (kurz)' )
    kurzform.allow_tags = False

    class Meta:
        ordering = ['-creation']
        verbose_name = _( u'Kontakt' )
        verbose_name_plural = _( u'Kontakte' )
