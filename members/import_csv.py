#-*- coding: utf-8 -*-

from seishinkan.utils import UnicodeReader
from datetime import datetime

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

        if 'j' == row[16].lower().strip():
            m.status = 3 # Ehrenmitglied

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
