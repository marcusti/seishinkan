#-*- coding: utf-8 -*-

from datetime import date, datetime
from django import get_version
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, mail_admins, send_mail, send_mass_mail
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from seishinkan import settings
from seishinkan.links.models import Link, LinkKategorie
from seishinkan.news.models import News
from seishinkan.website.forms import LoginForm, KontaktForm
from seishinkan.website.models import Artikel, Bild, Download, Seite, Termin, TrainingManager, Trainingsart, Wochentag
import captcha
import os

def __get_sidebar( request ):
    heute = int( datetime.today().strftime( '%w' ) )

    ctx = { }
    ctx['sidebar'] = True
    ctx['seiten'] = Seite.public_objects.filter( parent__isnull = True ).order_by( 'position' )
    ctx['language'] = request.session.get( 'django_language', 'de' )
    ctx['training_heute'] = TrainingManager().get_einheiten_pro_tag( heute )
    ctx['path'] = request.path
    ctx['host'] = request.META['HTTP_HOST']
    ctx['django_version'] = get_version()

    try:
        ctx['wochentag'] = Wochentag.objects.get( id = heute )
    except:
        pass

    if request.user.is_authenticated():
        ctx['users'] = User.objects.all().order_by( '-last_login' )

    return ctx

def index( request, sid = 1 ):
    ctx = __get_sidebar( request )

    seite = get_object_or_404( Seite.public_objects, id = sid )
    ctx['seite'] = seite
    ctx['artikel'] = Artikel.public_objects.get_by_category( sid )
    ctx['termine'] = Termin.public_objects.current()
    ctx['alle_termine'] = Termin.public_objects.all()
    ctx['beitraege'] = News.public_objects.all()

    if seite.show_training:
        ctx['wochenplan'] = TrainingManager().get_wochenplan()
        ctx['wochentage'] = TrainingManager().get_wochentage()
        ctx['trainingsarten'] = Trainingsart.objects.filter( public = True )

    return __create_response( request, ctx )

def dynamic_url( request, sitename = '' ):
    if not sitename or sitename.strip() == '':
        return index( request )

    seite = get_object_or_404( Seite.public_objects, url__iexact = sitename )
    return index( request, seite.id )

def kontakt( request ):
    ctx = __get_sidebar( request )

    if request.method == 'POST':
        # Check the captcha
        challenge_field = request.POST['recaptcha_challenge_field']
        response_field = request.POST['recaptcha_response_field']
        remote = request.META['REMOTE_ADDR']

        check_captcha = captcha.submit( challenge_field, response_field, settings.RECAPTCHA_PRIVATE_KEY, remote )

        if check_captcha.is_valid is False:
            # Captcha is wrong, show an error ...
            ctx['form'] = KontaktForm( request.POST )
            ctx['captcha_error'] = True
            ctx['html_captcha'] = captcha.displayhtml( settings.RECAPTCHA_PUB_KEY )
            return __create_response( request, ctx, 'kontakt.html' )

        form = KontaktForm( request.POST )
        if form.is_valid():
            # Sending mail...

            # An die Admins der Webanwendung:
            # mail_admins(form.data['subject'], form.data['message'], fail_silently=False)

            marcus = User.objects.get( username__iexact = 'marcus' )
            ecki = User.objects.get( username__iexact = 'ecki' )
            bert = User.objects.get( username__iexact = 'bert' )

            to_users = []
            bcc_users = [ marcus ]

            from_email = form.data['email']
            subject = '%s%s' % ( settings.EMAIL_SUBJECT_PREFIX, form.data['subject'] )
            message = '%s\n\n%s' % ( form.data['message'], settings.EMAIL_MESSAGE_POSTFIX )

            to_list = bcc_list = []

            for user in to_users:
                if user.email:
                    to_list.append( user.email )

            for user in bcc_users:
                if user.email:
                    bcc_list.append( user.email )

            if to_list or bcc_list:
                email = EmailMessage( subject, message, from_email, to_list, bcc_list )
                email.send()
            else:
                raise Exception( _( 'Keine Email Empfänger angegeben!' ) )

            ctx['form'] = form
            return __create_response( request, ctx, 'kontakt_ok.html' )
    else:
        form = KontaktForm()

    html_captcha = captcha.displayhtml( settings.RECAPTCHA_PUB_KEY )
    ctx['form'] = form
    ctx['html_captcha'] = html_captcha

    return __create_response( request, ctx, 'kontakt.html' )

def impressum( request ):
    ctx = __get_sidebar( request )

    return __create_response( request, ctx, 'impressum.html' )

def info( request ):
    ctx = __get_sidebar( request )

    return __create_response( request, ctx, 'info.html' )

def sysinfo( request ):
    ctx = __get_sidebar( request )

    bilder = Bild.objects.all()
    in_use = []
    for bild in bilder:
        in_use.append( bild.bild )
        in_use.append( bild.vorschau )
    ctx['bilder'] = bilder

    files = []
    path = 'bilder'
    for name in os.listdir( os.path.join( settings.MEDIA_ROOT, path ) ):
        files.append( os.path.join( path, name ) )
    path = os.path.join( 'bilder', 'thumbs' )
    for name in os.listdir( os.path.join( settings.MEDIA_ROOT, path ) ):
        files.append( os.path.join( path, name ) )

    files.sort()
    ctx['files'] = files

    no_use = []
    for file in files:
        abs_file = os.path.join( settings.MEDIA_ROOT, file )
        if not file in in_use and not os.path.isdir( abs_file ):
            no_use.append( file )
            #os.remove( abs_file )
    ctx['not_used'] = no_use

    return __create_response( request, ctx, 'sysinfo.html' )

def seishinkan_login( request ):
    ctx = __get_sidebar( request )
    ctx['next'] = request.GET.get( 'next', settings.LOGIN_REDIRECT_URL )

    if request.method == 'POST':
        form = LoginForm( request.POST )
        if form.is_valid():
            # user authentication is done in LoginForm validation
            user = form.get_user()
            login( request, user )

            if request.has_key( 'next' ):
                next = request['next']
            else:
                next = settings.LOGIN_REDIRECT_URL

            return redirect_to( request, next )
    else:
        form = LoginForm()

    ctx['form'] = form

    return __create_response( request, ctx, 'login.html' )

def seishinkan_logout( request ):
    logout( request )

    if request.META['HTTP_REFERER']:
        return HttpResponseRedirect( request.META['HTTP_REFERER'] )

    return index( request )

def links( request ):
    ctx = __get_sidebar( request )

    ctx['links'] = Link.public_objects.all()
    ctx['kategorien'] = LinkKategorie.public_objects.all()

    return __create_response( request, ctx, 'links.html' )

def bilder( request ):
    ctx = __get_sidebar( request )

    return __create_response( request, ctx, 'bilder.html' )

def downloads( request ):
    ctx = __get_sidebar( request )
    ctx['downloads'] = Download.public_objects.all()

    return __create_response( request, ctx, 'downloads.html' )

def news( request, bid = None ):
    ctx = __get_sidebar( request )

    if bid:
        ctx['beitrag'] = get_object_or_404( News.public_objects, id = bid )
        return __create_response( request, ctx, 'news.html' )
    else:
        ctx['beitraege'] = News.public_objects.all()
        return __create_response( request, ctx, 'news_list.html' )

def video( request, vid = None ):
    ctx = __get_sidebar( request )

    import youtube
    client = youtube.YouTubeClient( 'gmsnG0W2bTA' )
    ctx['videos'] = client.list_by_user( 'eckido', page = 1, per_page = 10 )

    if vid:
        video = client.get_details( vid )
        if video:
            ctx['vid'] = vid
            ctx['watch'] = video

    return __create_response( request, ctx, 'videos.html' )

def termin( request, tid = None ):
    ctx = __get_sidebar( request )

    if tid:
        ctx['termin'] = get_object_or_404( Termin.public_objects, id = tid )
        return __create_response( request, ctx, 'termin.html' )
    else:
        ctx['alle_termine'] = Termin.public_objects.all()
        return __create_response( request, ctx, 'termine_list.html' )

def __create_response( request, context = {}, template_name = 'base.html' ):
    return render_to_response(
        template_name,
        context,
        context_instance = RequestContext( request ),
    )
