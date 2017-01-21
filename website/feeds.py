#-*- coding: utf-8 -*-

from datetime import datetime
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from seishinkan.website.models import Termin
from seishinkan.news.models import News

class TerminFeed( Feed ):
    feed_type = Atom1Feed
    title = u'Seishinkan Termine'
    link = u'/termine/'
    subtitle = u'Termine und Veranstaltungen des Aikido Dojo Seishinkan, www.aikido-dojo-seishinkan.de'

    def items( self ):
        return Termin.public_objects.all()[:30]

    def item_pubdate( self, item ):
        try:
            #return item.modified
            b = item.beginn
            return datetime( b.year, b.month, b.day )
        except:
            pass

class NewsFeed( Feed ):
    feed_type = Atom1Feed
    title = u'Seishinkan News'
    link = u'/news/'
    subtitle = u'Artikel und Neuigkeiten aus dem Aikido Dojo Seishinkan, www.aikido-dojo-seishinkan.de'

    def items( self ):
        return News.public_objects.all()[:30]

    def item_pubdate( self, item ):
        try:
            return item.modified
        except:
            pass

    def item_author_name( self, item ):
        try:
            s = ''
            for author in item.autoren.iterator():
                if len( s ) > 0:
                    s += ', %s' % author
                else:
                    s += str ( author )
            return s.strip()
        except:
            pass
