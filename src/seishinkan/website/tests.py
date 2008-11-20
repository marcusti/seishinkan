#-*- coding: utf-8 -*-

from django.core import mail
from django.test import TestCase
from seishinkan import settings
from seishinkan.website.models import Seite

NAME_START = 'Start'
NAME_SUB = 'Sub'

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
