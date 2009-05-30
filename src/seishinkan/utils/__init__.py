#-*- coding: utf-8 -*-

from datetime import date
from django.db import models
from django.utils.translation import ugettext_lazy as _
import csv, codecs, cStringIO

DEFAULT_MAX_LENGTH = 200

def get_next_month( adate = date.today() ):
    try:
        if adate.month == 12:
            return date( adate.year + 1, 1, 1 )
        else:
            return date( adate.year, adate.month + 1, 1 )
    except:
        return None

class AbstractModel( models.Model ):
    public = models.BooleanField( _( u'Öffentlich' ), default = True, help_text = '' )
    creation = models.DateTimeField( _( u'Erfasst am' ), auto_now_add = True, help_text = '' )
    modified = models.DateTimeField( _( u'Geändert am' ), auto_now = True, help_text = '' )

    class Meta:
        abstract = True

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__( self, f, encoding ):
        self.reader = codecs.getreader( encoding )( f )

    def __iter__( self ):
        return self

    def next( self ):
        return self.reader.next().encode( "utf-8" )

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__( self, f, dialect = csv.excel, encoding = "utf-8", **kwds ):
        f = UTF8Recoder( f, encoding )
        self.reader = csv.reader( f, dialect = dialect, **kwds )

    def next( self ):
        row = self.reader.next()
        return [unicode( s, "utf-8" ) for s in row]

    def __iter__( self ):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__( self, f, dialect = csv.excel, encoding = "utf-8", **kwds ):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer( self.queue, dialect = dialect, **kwds )
        self.stream = f
        self.encoder = codecs.getincrementalencoder( encoding )()

    def writerow( self, row ):
        self.writer.writerow( [s.encode( "utf-8" ) for s in row] )
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode( "utf-8" )
        # ... and reencode it into the target encoding
        data = self.encoder.encode( data )
        # write to the target stream
        self.stream.write( data )
        # empty queue
        self.queue.truncate( 0 )

    def writerows( self, rows ):
        for row in rows:
            self.writerow( row )

def unicode_csv_reader( unicode_csv_data, dialect = csv.excel, **kwargs ):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader( utf_8_encoder( unicode_csv_data ), dialect = dialect, **kwargs )
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode( cell, 'utf-8' ) for cell in row]

def utf_8_encoder( unicode_csv_data ):
    for line in unicode_csv_data:
        yield line.encode( 'utf-8' )

#class XFieldList( list ):
#    """ List for field names.
#    Changes "*_" to specific field names for the current language,
#    i.e.
#    "sort_order" => "sort_order"
#    "title_" => "title", "title_de", or "title_es"
#    "__str__" => "__str__"
#    """
#    def __init__( self, sequence = [] ):
#        self.sequence = sequence
#    def __iter__( self ):
#        return iter( self._get_list() )
#    def __getitem__( self, k ):
#        return self._get_list()[k]
#    def __nonzero__( self ):
#        return bool( self.sequence )
#    def __len__( self ):
#        return len( self.sequence )
#    def __str__( self ):
#        return str( self._get_list() )
#    def __repr__( self ):
#        return repr( self._get_list() )
#    def _get_list( self ):
#        language = translation.get_language()[:2]
#        result = []
#        for item in self.sequence:
#            if item[:1] == "-":
#                order = "-"
#                item = item[1:]
#            else:
#                order = ""
#            if item[:2] == "__" or item[-1:] != "_":
#                result.append( order + item )
#            else:
#                if language == "de":
#                    result.append( order + item[:-1] )
#                else:
#                    result.append( order + item + language )
#        return result
