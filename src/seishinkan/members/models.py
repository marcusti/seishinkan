#-*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH, AbstractModel, UnicodeReader
from datetime import datetime
import csv

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
        return '%s (%s)' % ( self.name(), self.id )

    class Meta:
        ordering = ['vorname', 'nachname']
        verbose_name = _( u'Person' )
        verbose_name_plural = _( u'Personen' )

class MitgliederManager( models.Manager ):
    def get_query_set( self ):
        return super( MitgliederManager, self ).get_query_set().filter( public = True )

class Mitglied( Person ):
    status = models.IntegerField( _( u'Status' ), default = 1, choices = STATUS )
    mitglied_seit = models.DateField( _( u'Mitglied seit' ), blank = True, null = True )
    ist_vorstand = models.BooleanField( _( u'Vorstand' ), default = False )
    ist_trainer = models.BooleanField( _( u'Trainer' ), default = False )
    ist_kind = models.BooleanField( _( u'Kind' ), default = False )

    objects = models.Manager()
    public_objects = MitgliederManager()

    def aktuelle_graduierung( self ):
        return self.graduierung_set.latest( 'datum' )
    aktuelle_graduierung.short_description = _( u'Graduierung' )
    aktuelle_graduierung.allow_tags = True

    def __unicode__( self ):
        return super( Mitglied, self ).__unicode__()

    class Meta( Person.Meta ):
        verbose_name = _( u'Mitglied' )
        verbose_name_plural = _( u'Mitglieder' )

class Graduierung( AbstractModel ):
    person = models.ForeignKey( Person, verbose_name = _( u'Person' ) )
    datum = models.DateField( _( u'Datum' ), blank = True, null = True )
    graduierung = models.IntegerField( _( u'Graduierung' ), choices = GRADUIERUNGEN )
    text = models.TextField( _( u'Text' ), blank = True )

    def __unicode__( self ):
        return self.name()

    class Meta:
        ordering = ['graduierung']
        verbose_name = _( u'Graduierung' )
        verbose_name_plural = _( u'Graduierungen' )

def import_mitglieder( filename = 'members/mitglieder.csv'):
    for row in UnicodeReader( open( filename, 'rb' ) ):
        m = Mitglied()
        m.public = True
        m.creation = datetime.now().strftime( '%Y-%m-%d %H:%M:%S' )
        m.modified = datetime.now().strftime( '%Y-%m-%d %H:%M:%S' )
        m.id = row[0]
        m.nachname = row[1]
        m.vorname = row[2]
        m.plz = row[3]
        m.stadt = row[4]
        m.strasse = row[5]
        m.fon = row[6]
        m.mobil = row[7]
        m.fax = row[8]
        m.email = row[9]

        if 'j' == row[14].lower().strip():
            m.status = 2 # Passiv

        if 'n' == row[15].lower().strip():
            m.status = 0 # Austritt

        if 'j' == row[17].lower().strip():
            m.ist_vorstand = True

        if 'j' == row[18].lower().strip():
            m.ist_trainer = True

        if 'j' == row[19].lower().strip():
            m.ist_kind = True

        try:
            m.geburt = datetime.strptime( row[10], '%d.%m.%Y' ).strftime( '%Y-%m-%d' )
        except:
            pass

        try:
            m.mitglied_seit = datetime.strptime( row[11], '%d.%m.%Y' ).strftime( '%Y-%m-%d' )
        except:
            pass

        m.save()
        print m


        # Graduierungen...



        if row[12]:
            for gid, grad in GRADUIERUNGEN:
                if grad == row[12]:
                    try:
                        gdatum = datetime.strptime( row[13], '%d.%m.%Y' ).strftime( '%Y-%m-%d' )
                    except:
                        print m
                        gdatum = None
                
                    g, created = Graduierung.objects.get_or_create( person = m, graduierung = gid, datum = gdatum,
                                                                    defaults = {
                            'person': m,
                            'datum': gdatum,
                            'graduierung': gid,
                            })

                    g.save()
