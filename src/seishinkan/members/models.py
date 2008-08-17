#-*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH, AbstractModel

STATUS = [
    ( 0, _( u'Austritt' ) ),
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
]

class Person( AbstractModel ):
    vorname = models.CharField( _( u'Vorname' ), max_length = DEFAULT_MAX_LENGTH )
    nachname = models.CharField( _( u'Nachname' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    plz = models.CharField( _( u'PLZ' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    stadt = models.CharField( _( u'Stadt' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    strasse = models.CharField( _( u'Straße' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    fon = models.CharField( _( u'Telefon' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    fax = models.CharField( _( u'Telefax' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    mobil = models.CharField( _( u'Handy' ), max_length = DEFAULT_MAX_LENGTH, blank = True )
    email = models.EmailField( _( u'E-Mail' ), blank = True )
    geburt = models.DateField( _( u'Geburt' ), blank = True, null = True )
    text = models.TextField( _( u'Text' ), blank = True )

    def name( self ):
        return ( '%s %s' % ( self.vorname, self.nachname ) ).strip()
    name.short_description = _( u'Name' )
    name.allow_tags = True

    def __unicode__( self ):
        return self.name()

    class Meta:
        ordering = ['vorname', 'nachname']
        verbose_name = _( u'Person' )
        verbose_name_plural = _( u'Personen' )

class Mitglied( Person ):
    status = models.IntegerField( _( u'Status' ), default = 1, choices = STATUS )
    nummer = models.IntegerField( _( u'Nummer' ) )
    mitglied_seit = models.DateField( _( u'Mitglied seit' ), blank = True, null = True )
    ist_vorstand = models.BooleanField( _( u'Vorstand' ), default = False )
    ist_trainer = models.BooleanField( _( u'Trainer' ), default = False )
    ist_kind = models.BooleanField( _( u'Kind' ), default = False )

    def __unicode__( self ):
        return Person.__unicode__()

    class Meta( Person.Meta ):
        verbose_name = _( u'Mitglied' )
        verbose_name_plural = _( u'Mitglieder' )

class Graduierung( AbstractModel ):
    person = models.ForeignKey( Person, verbose_name = _( u'Person' ) )
    datum = models.DateField( _( u'Datum' ) )
    graduierung = models.IntegerField( _( u'Graduierung' ), choices = GRADUIERUNGEN )
    text = models.TextField( _( u'Text' ), blank = True )

    def __unicode__( self ):
        return self.name()

    class Meta:
        ordering = ['graduierung']
        verbose_name = _( u'Graduierung' )
        verbose_name_plural = _( u'Graduierungen' )
