#-*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from seishinkan.utils import DEFAULT_MAX_LENGTH, AbstractModel

class Person( AbstractModel ):
    firstname = models.CharField( _( u'Vorname' ), max_length = DEFAULT_MAX_LENGTH )
    lastname = models.CharField( _( u'Nachname' ), max_length = DEFAULT_MAX_LENGTH, blank = True )

    def name( self ):
        return ( '%s %s' % ( self.firstname, self.lastname ) ).strip()
    name.short_description = _( u'Name' )
    name.allow_tags = True

    def __unicode__( self ):
        return self.name()

    class Meta:
        ordering = ['firstname', 'lastname']
        verbose_name = _( u'Person' )
        verbose_name_plural = _( u'Personen' )
