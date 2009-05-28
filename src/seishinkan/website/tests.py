#-*- coding: utf-8 -*-

from datetime import date
from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.conf import settings
from seishinkan.website.models import Seite
from seishinkan.utils import get_next_month

NAME_START = 'Start'
NAME_SUB = 'Sub'

class UtilsTest( TestCase ):
    def testNextMonth( self ):
        self.assertEquals( get_next_month( date( 2008, 12, 29 ) ), date( 2009, 1, 1 ) )
        self.assertEquals( get_next_month( date( 2009, 1, 1 ) ), date( 2009, 2, 1 ) )

class EmailTest( TestCase ):
    def setUp( self ):
        self.SUBJECT = 'Hallo'
        self.BODY = 'Django UnitTest Email'

    def testAdminEmail( self ):
        mail.mail_admins( self.SUBJECT, self.BODY )
        self.assertEquals( len( mail.outbox ), 1 )
        self.assertEquals( mail.outbox[0].subject, settings.EMAIL_SUBJECT_PREFIX + self.SUBJECT )

    def testStratoEmail( self ):
        con = mail.SMTPConnection( host = settings.STRATO_EMAIL_HOST, username = settings.STRATO_EMAIL_HOST_USER, password = settings.STRATO_EMAIL_HOST_PASSWORD, use_tls = settings.STRATO_EMAIL_USE_TLS )
        self.failIf( con is None )

        email = mail.EmailMessage()
        email.subject = self.SUBJECT
        email.body = self.BODY
        email.from_email = settings.TEST_EMAIL
        email.to = [ settings.TEST_EMAIL, settings.ADMINS[0][1] ]
        email.connection = con
        email.send()
        self.assertEquals( len( mail.outbox ), 1 )

class SeiteTest( TestCase ):
    def setUp( self ):
        # disable SSL redirects
        settings.SSL_URLS = []

        # create a user account in test database
        user = User.objects.create_user( 'super', '', 'super' )
        user.is_staff = True
        user.is_superuser = True
        user.save()

        # create some sites
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

    def testLogin( self ):
        c = Client()
        self.failIf( c.login( username = 'super', password = 'toll' ) )
        self.failIf( c.login( username = 'bla', password = 'blubb' ) )
        self.failUnless( c.login( username = 'super', password = 'super' ) )

    def testMitgliederlisten( self ):
        c = Client()
        self.failUnless( c.login( username = 'super', password = 'super' ) )

        response = c.post( '/mitglieder/' )
        self.assertEquals( response.status_code, 200 )
        self.assert_( response.context is not None )

        # get latest context in list of rendered contexts
        ctx = response.context[ len( response.context ) - 1 ]
        self.assertEquals( ctx['menu'], 'mitglieder' )
        self.failUnless( ctx['months'] is not None )
