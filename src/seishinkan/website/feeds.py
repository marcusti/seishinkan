#-*- coding: utf-8 -*-

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from seishinkan.website.models import Termin
from seishinkan.news.models import News

class TerminFeed( Feed ):
    feed_type = Atom1Feed
    title = u'aikido-dojo-seishinkan.de, Termine'
    link = u'/termine/'
    subtitle = u'Termine und Veranstaltungen des Aikido Dojo Seishinkan'

    def items( self ):
        return Termin.public_objects.all()[:30]

    def item_pubdate( self, item ):
        try:
            return item.modified
        except:
            pass

class NewsFeed( Feed ):
    feed_type = Atom1Feed
    title = u'aikido-dojo-seishinkan.de, News'
    link = u'/news/'
    subtitle = u'Artikel und Neuigkeiten aus dem Aikido Dojo Seishinkan'

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
                s = '%s %s' % ( s, author )
            return s.strip()
        except:
            raise
