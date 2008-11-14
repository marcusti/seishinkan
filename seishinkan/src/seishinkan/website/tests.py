#-*- coding: utf-8 -*-

import unittest
from django.test import TestCase
from seishinkan.website.models import Seite

NAME_START = 'Start'
NAME_SUB = 'Sub'

class SeiteTest( TestCase ):
    def setUp( self ):
        self.startseite = Seite.objects.create( name = NAME_START, url = NAME_START.lower(), is_homepage = True )
        self.subseite = Seite.objects.create( name = NAME_SUB, url = NAME_SUB.lower(), parent = self.startseite )

    def testStart( self ):
        self.failIf( self.startseite.public is False )
        self.failIf( self.startseite.is_homepage is False )
        self.failUnless( self.startseite.parent is None )
        self.assertEquals( self.startseite.get_name(), NAME_START )

    def testSub( self ):
        self.failIf( self.subseite.public is False )
        self.failIf( self.subseite.is_homepage is True )
        self.assertEquals( self.subseite.parent, self.startseite )
        self.assertEquals( self.subseite.get_name(), NAME_SUB )
