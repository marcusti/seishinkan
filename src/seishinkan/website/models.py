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

class WochentagAdmin( admin.ModelAdmin ):
    ordering = ['index', 'name']
    list_display = ( 'name', 'public', 'creation', 'modified', 'index' )

admin.site.register( Wochentag, WochentagAdmin )

class BildManager( models.Manager ):
    def get_query_set( self ):
        return super( BildManager, self ).get_query_set().filter( public = True )

class Bild( models.Model ):
    name = models.CharField( _( u'Titel' ), max_length = DEFAULT_MAX_LENGTH, blank = True, unique = True )
    bild = models.ImageField( _( u'Pfad' ), upload_to = 'bilder/' )
    vorschau = models.ImageField( _( u'Vorschau' ), upload_to = 'bilder/thumbs/', blank = True, editable = False )
    max_breit = models.IntegerField( _( u'max. Breite' ), default = 200 )
    max_hoch = models.IntegerField( _( u'max. Höhe' ), default = 200 )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = BildManager()

    def save( self ):
        if self.bild:
            if not self.name or self.name.strip() == '':
                self.name = self.get_bild_filename()
            from PIL import Image
            THUMBNAIL_SIZE = ( 75, 75 )
            SCALE_SIZE = ( self.max_breit, self.max_hoch )
            if not self.vorschau:
                self.save_vorschau_file( self.get_bild_filename(), '' )
            image = Image.open( self.get_bild_filename() )
            image.thumbnail( SCALE_SIZE, Image.ANTIALIAS )
            image.save( self.get_bild_filename() )
            if image.mode not in ( 'L', 'RGB' ):
                image = image.convert( 'RGB' )
            image.thumbnail( THUMBNAIL_SIZE, Image.ANTIALIAS )
            image.save( self.get_vorschau_filename() )
            super( Bild, self ).save()

    def admin_thumb( self ):
        w = self.get_vorschau_width()
        h = self.get_vorschau_height()
        return u'<img src="%s" width="%s" height="%s" />' % ( self.get_vorschau_url(), w, h )
    admin_thumb.short_description = _( u'Bild' )
    admin_thumb.allow_tags = True

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _( u'Bild' )
        verbose_name_plural = _( u'Bilder' )

class BildAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'bild', 'max_breit', 'max_hoch', 'modified', 'admin_thumb' )
    list_display_links = ( 'name', 'admin_thumb' )
    search_fields = [ 'name', 'bild' ]

admin.site.register( Bild, BildAdmin )

class TitelBild( Bild ):
    
    class Meta:
        ordering = ['name']
        verbose_name = _( u'Bild im Kopf' )
        verbose_name_plural = _( u'Bilder im Kopf' )

admin.site.register( TitelBild, BildAdmin )
   
class SeitenManager( models.Manager ):
    def get_query_set( self ):
        return super( SeitenManager, self ).get_query_set().filter( public = True )

    def get_homepage( self ):
        homepages = self.get_query_set().filter( is_homepage = True )
        if homepages.count() > 0:
            return homepages[0]
        else:
            return None

class Seite( models.Model ):
    name = models.CharField( _( u'Name' ), max_length = DEFAULT_MAX_LENGTH )
    name_en = models.CharField( _( u'Name (Englisch)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    name_ja = models.CharField( _( u'Name (Japanisch)' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    url = models.SlugField( _( u'URL' ), unique = True, max_length = DEFAULT_MAX_LENGTH )
    position = models.IntegerField( _( u'Position im Menü' ), default = 0 )
    parent = models.ForeignKey( 'self', verbose_name = _( u'Über' ), null = True, blank = True, related_name = 'child_set' )
    titelbild = models.ForeignKey( TitelBild, verbose_name = u'Bild im Kopf', blank = True, null = True )
    show_training = models.BooleanField( _( u'Enthält Trainingszeiten' ), default = False )
    is_homepage = models.BooleanField( _( u'Ist Startseite' ), default = False )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = SeitenManager()

    def get_titelbild( self ):
        hp = self.public_objects.get_homepage()
        
        if self.titelbild:
            return self.titelbild
        elif self.parent and self.parent.titelbild:
            return self.parent.titelbild
        elif hp and hp.titelbild:
            return hp.titelbild

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

class SeiteAdmin( admin.ModelAdmin ):
    prepopulated_fields = {'url': ( 'name', )}
    ordering = ['name']
    search_fields = [ 'name' ]
    list_display = ( 'name', 'url', 'parent', 'position', 'is_homepage', 'public', 'id' )
    list_filter = ( 'parent', )

admin.site.register( Seite, SeiteAdmin )

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
    text_src = models.CharField( _( u'Code' ), max_length = 5000, blank = True )
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

class ArtikelAdmin( admin.ModelAdmin ):
    ordering = ['title', 'text']
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

admin.site.register( Artikel, ArtikelAdmin )

class TerminManager( models.Manager ):
    def get_query_set( self ):
        return super( TerminManager, self ).get_query_set().filter( public = True ).order_by( '-ende', '-beginn', 'title' )

    def current( self ):
        heute = date.today()
        return self.get_query_set().filter( Q( beginn__gte = heute ) | Q( ende__gte = heute ) ).order_by( 'ende', 'beginn', 'title' )

class Termin( models.Model ):
    title = models.CharField( _( u'Überschrift' ), max_length = DEFAULT_MAX_LENGTH )
    text = models.TextField( _( u'Text' ) )
    ort = models.CharField( _( u'Ort' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    bild = models.ForeignKey( Bild, verbose_name = u'Bild', blank = True, null = True )
    bild_ausrichtung = models.CharField( _( u'Bild Ausrichtung' ), max_length = DEFAULT_MAX_LENGTH, choices = AUSRICHTUNGEN, default = u'right', blank = True )
    beginn = models.DateField( _( u'Beginn' ) )
    ende = models.DateField( _( u'Ende' ) )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = TerminManager()

    def get_absolute_url( self ):
        return '/termin/%i/' % self.id

    def __unicode__( self ):
        return u'%s'.strip() % ( self.title )

    class Meta:
        ordering = ['ende', 'beginn', 'title']
        verbose_name = _( u'Termin' )
        verbose_name_plural = _( u'Termine' )

class TerminAdmin( admin.ModelAdmin ):
    ordering = ['ende', 'beginn', 'title']
    search_fields = [ 'title', 'text', 'ort' ]
    list_display = ( 'title', 'ort', 'beginn', 'ende', 'bild', 'modified', 'public', 'id' )
    list_filter = ( 'beginn', 'ende', 'ort' )

    class Media:
        js = ( '/static/js/tiny_mce/tiny_mce.js',
              '/static/js/textareas.js', )

admin.site.register( Termin, TerminAdmin )

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

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    def get_name( self, language = None ):
        return getattr( self, "name_%s" % ( language or translation.get_language()[:2] ), "" ) or self.name

    def __unicode__( self ):
        return u'%s'.strip() % ( self.get_name() )

    class Meta:
        ordering = ['name']
        verbose_name = _( u'Trainingsart' )
        verbose_name_plural = _( u'Trainingsarten' )

class TrainingsartAdmin( admin.ModelAdmin ):
    ordering = ['name']
    list_display = ( 'name', 'creation', 'modified', 'public', 'id' )

admin.site.register( Trainingsart, TrainingsartAdmin )

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

class TrainingAdmin( admin.ModelAdmin ):
    ordering = ['wochentag', 'von']
    list_display = ( 'wochentag', 'von', 'bis', 'art', 'creation', 'modified', 'public' )

admin.site.register( Training, TrainingAdmin )

class DownloadManager( models.Manager ):
    def get_query_set( self ):
        return super( DownloadManager, self ).get_query_set().filter( public = True )

class Download( models.Model ):
    name = models.CharField( _( u'Name' ), max_length = DEFAULT_MAX_LENGTH )
    text = models.TextField( _( u'Text' ) )
    datei = models.FileField( _( u'Pfad' ), upload_to = 'downloads/' )

    public = models.BooleanField( _( u'Öffentlich' ), default = True )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True )

    objects = models.Manager()
    public_objects = DownloadManager()

    def extension( self ):
        root, ext =  os.path.splitext( self.datei )
        if ext and len( ext ) > 0:
            if ext.startswith( '.' ):
                return ext.lower()[1:]
            else:
                return ext.lower()
        return ''

    def __unicode__( self ):
        return u'%s %s'.strip() % ( self.name, self.datei )

    def get_absolute_url( self ):
        return '/downloads/'

    class Meta:
        ordering = ['-modified']
        verbose_name = _( u'Download' )
        verbose_name_plural = _( u'Downloads' )

class DownloadAdmin( admin.ModelAdmin ):
    ordering = [ '-modified' ]
    search_fields = [ 'name', 'text', 'datei' ]
    list_display = ( 'name', 'datei', 'modified', 'public' )

admin.site.register( Download, DownloadAdmin )

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

class KontaktAdmin( admin.ModelAdmin ):
    ordering = [ '-creation' ]
    search_fields = [ 'sender', 'betreff', 'nachricht' ]
    list_display = ( 'sender', 'betreff', 'kurzform', 'creation' )
    list_display_links = ( 'sender', 'betreff', 'kurzform' )

admin.site.register( Kontakt, KontaktAdmin )
