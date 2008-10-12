#-*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH, AbstractModel
from seishinkan.website.templatetags.seishinkan_tags import *

STATUS = [
    ( 0, _( u'Nicht Mitglied' ) ),
    ( 1, _( u'Aktiv' ) ),
    ( 2, _( u'Passiv' ) ),
    ( 3, _( u'Ehrenmitglied' ) ),
]

GRADUIERUNGEN = [
    ( 1000, _( u'10. Dan' ) ),
    ( 900,   _( u'9. Dan' ) ),
    ( 800,   _( u'8. Dan' ) ),
    ( 700,   _( u'7. Dan' ) ),
    ( 600,   _( u'6. Dan' ) ),
    ( 500,   _( u'5. Dan' ) ),
    ( 400,   _( u'4. Dan' ) ),
    ( 300,   _( u'3. Dan' ) ),
    ( 200,   _( u'2. Dan' ) ),
    ( 100,   _( u'1. Dan' ) ),

    ( 50,    _( u'1. Kyu' ) ),
    ( 40,    _( u'2. Kyu' ) ),
    ( 30,    _( u'3. Kyu' ) ),
    ( 20,    _( u'4. Kyu' ) ),
    ( 10,    _( u'5. Kyu' ) ),

    ( -10,    _( u'1.2 Kinder-Kyu' ) ),
    ( -11,    _( u'1.1 Kinder-Kyu' ) ),
    ( -20,    _( u'2.2 Kinder-Kyu' ) ),
    ( -21,    _( u'2.1 Kinder-Kyu' ) ),
    ( -30,    _( u'3.2 Kinder-Kyu' ) ),
    ( -31,    _( u'3.1 Kinder-Kyu' ) ),
    ( -40,    _( u'4.2 Kinder-Kyu' ) ),
    ( -41,    _( u'4.1 Kinder-Kyu' ) ),
    ( -50,    _( u'5.2 Kinder-Kyu' ) ),
    ( -51,    _( u'5.1 Kinder-Kyu' ) ),
]

class Land( AbstractModel ):
    name = models.CharField( _( u'Name' ), max_length = DEFAULT_MAX_LENGTH )

    def __unicode__( self ):
        return self.name

    class Meta:
        ordering = [ 'name' ]
        verbose_name = _( u'Land' )
        verbose_name_plural = _( u'Länder' )

class MitgliederManager( models.Manager ):
    def get_query_set( self ):
        return super( MitgliederManager, self ).get_query_set().filter( public = True )

class Mitglied( AbstractModel ):
    vorname = models.CharField( _( u'Vorname' ), max_length = DEFAULT_MAX_LENGTH )
    nachname = models.CharField( _( u'Nachname' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    plz = models.CharField( _( u'PLZ' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    stadt = models.CharField( _( u'Stadt' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    strasse = models.CharField( _( u'Straße' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    land = models.ForeignKey( Land, verbose_name = _( u'Land' ), default = 1, blank = True, null = True )
    fon = models.CharField( _( u'Telefon' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    fax = models.CharField( _( u'Telefax' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    mobil = models.CharField( _( u'Handy' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    email = models.EmailField( _( u'E-Mail' ), blank = True )
    geburt = models.DateField( _( u'Geburt' ), blank = True, null = True )
    text = models.TextField( _( u'Text' ), blank = True )

    status = models.IntegerField( _( u'Status' ), default = 1, choices = STATUS )
    mitglied_seit = models.DateField( _( u'Mitglied seit' ), blank = True, null = True )
    austritt_am = models.DateField( _( u'Austritt am' ), blank = True, null = True )
    ist_vorstand = models.BooleanField( _( u'Vorstand' ), default = False )
    ist_trainer = models.BooleanField( _( u'Trainer' ), default = False )
    ist_kind = models.BooleanField( _( u'Kind' ), default = False )
    bekommt_emails = models.BooleanField( _( u'bekommt Emails' ), default = True )

    objects = models.Manager()
    public_objects = MitgliederManager()

    def name( self ):
        return ( u'%s %s' % ( self.vorname, self.nachname ) ).strip()
    name.short_description = _( u'Name' )
    name.allow_tags = True

    def alter( self ):
        return age( self.geburt )
    alter.short_description = _( u'Alter' )
    alter.allow_tags = True

    def ist_mitglied( self ):
        return not self.status == 0

    def ist_aktiv( self ):
        return self.status == 1

    def ist_passiv( self ):
        return self.status == 2

    def ist_ehrenmitglied( self ):
        return self.status == 3

    def __unicode__( self ):
        return self.name()

    def aktuelle_graduierung( self ):
        return self.graduierung_set.latest( 'datum' )
    aktuelle_graduierung.short_description = _( u'Graduierung' )
    aktuelle_graduierung.allow_tags = True

    class Meta:
        ordering = [ 'vorname', 'nachname' ]
        verbose_name = _( u'Mitglied' )
        verbose_name_plural = _( u'Mitglieder' )

class Graduierung( AbstractModel ):
    person = models.ForeignKey( Mitglied, verbose_name = _( u'Person' ) )
    datum = models.DateField( _( u'Datum' ), blank = True, null = True )
    graduierung = models.IntegerField( _( u'Graduierung' ), choices = GRADUIERUNGEN )
    text = models.TextField( _( u'Text' ), blank = True )

    def __unicode__( self ):
        return self.get_graduierung_display()

    class Meta:
        ordering = ['-graduierung']
        verbose_name = _( u'Graduierung' )
        verbose_name_plural = _( u'Graduierungen' )
