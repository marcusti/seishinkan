#-*- coding: utf-8 -*-

from datetime import date, datetime
from django import get_version
from django.contrib.admin.models import LogEntry
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins, send_mail, send_mass_mail
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.i18n import set_language
from seishinkan import settings
from seishinkan.links.models import Link, LinkKategorie
from seishinkan.news.models import News
from seishinkan.website.forms import LoginForm, KontaktForm
from seishinkan.website.models import *
from seishinkan.members.models import *
from seishinkan.utils import UnicodeWriter
import captcha
import os

def __get_sidebar( request ):
    heute = int( datetime.today().strftime( '%w' ) )

    ctx = { }
    ctx['sidebar'] = True
    ctx['seiten'] = Seite.public_objects.filter( parent__isnull = True ).order_by( 'position' )
    ctx['language'] = request.session.get( 'django_language', 'de' )
    ctx['training_heute'] = TrainingManager().get_einheiten_pro_tag( heute )
    ctx['termine_heute'] = Termin.public_objects.current()
    ctx['training_aktuell'] = TrainingAktuell.public_objects.get_aktuelle_meldungen()
    ctx['path'] = request.path
    ctx['host'] = request.META['HTTP_HOST']
    ctx['django_version'] = get_version()
    ctx['homepage'] = Seite.public_objects.get_homepage()

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
    ctx['menu'] = seite.url
    ctx['artikel'] = Artikel.public_objects.get_by_category( sid )

    if seite.show_events:
        ctx['termine'] = Termin.public_objects.current()
        ctx['anzahl_termine'] = Termin.public_objects.all().count()
        
    if seite.show_news:
        ctx['beitraege'] = News.public_objects.all()

    if seite.show_training:
        ctx['wochenplan'] = TrainingManager().get_wochenplan()
        ctx['wochentage'] = TrainingManager().get_wochentage()
        ctx['trainingsarten'] = Trainingsart.objects.filter( public = True )

    if seite.show_anfaenger:
        anfaengerkurse = Training.objects.filter( public = True, art__ist_anfaengerkurs = True )
        if anfaengerkurse and anfaengerkurse.count() > 0:
            ctx['anfaengerkurs_liste'] = anfaengerkurse
            ctx['anfaengerkurs'] = anfaengerkurse[0].art
        
    if seite.show_kinder:
        kindertraining = Training.objects.filter( public = True, art__ist_kindertraining = True )
        if kindertraining and kindertraining.count() > 0:
            ctx['kindertraining_liste'] = kindertraining
            ctx['kindertraining'] = kindertraining[0].art
        
    return __create_response( request, ctx )

def dynamic_url( request, sitename = '' ):
    if not sitename or sitename.strip() == '':
        return index( request )

    seite = get_object_or_404( Seite.public_objects, url__iexact = sitename )
    return index( request, seite.id )

def kontakt( request ):
    ctx = __get_sidebar( request )
    ctx['menu'] = 'kontakt'

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

            marcus = User.objects.get( username__iexact = 'marcus' )
            ecki = User.objects.get( username__iexact = 'ecki' )
            bert = User.objects.get( username__iexact = 'bert' )
            ralf = User.objects.get( username__iexact = 'ralf' )

            to_users = [ ecki, marcus ]

            name = form.data['name']
            if name:
                from_email = '%s <%s>' % ( name, form.data['email'] )
            else:
                from_email = form.data['email']
            subject = '%s%s' % ( settings.EMAIL_SUBJECT_PREFIX, form.data['subject'] )
            message = '%s\n\n%s' % ( form.data['message'], settings.EMAIL_MESSAGE_POSTFIX )

            to_list = []
            for user in to_users:
                if user.email:
                    to_list.append( user.email )

            mails = []

            # Wenn gewünscht, Kopie an den Absender...
            if form.data.get( 'copy_to_me', False ):
                to_list.append( from_email )

            # Je eine Mail an die ausgewählten User senden...
            for email in to_list:
                mails.append( ( subject, message, from_email, [email] ) )
            
            send_mass_mail( mails )
            
            # An die Admins der Webanwendung: 
            # mail_admins( subject, message, fail_silently=False)

            # In Datenbank speichern...
            kontakt = Kontakt( sender = from_email, betreff = subject, nachricht = message )
            kontakt.captcha = request.POST['recaptcha_response_field']
            to_text = ''

            for email in to_list:
                to_text += '%s;' % email

            if to_text.endswith( ';' ):
                to_text = to_text[:-1]

            kontakt.to = to_text
            kontakt.save()
            
            ctx['form'] = form
            return __create_response( request, ctx, 'kontakt_ok.html' )
    else:
        form = KontaktForm()

    html_captcha = captcha.displayhtml( settings.RECAPTCHA_PUB_KEY )
    ctx['form'] = form
    ctx['html_captcha'] = html_captcha

    return __create_response( request, ctx, 'kontakt.html' )

@login_required
def admin_log( request ):
    ctx = __get_sidebar( request )
    ctx['menu'] = 'admin_log'

    if request.user.is_authenticated():
        qs = LogEntry.objects.all().order_by( '-action_time' )
    else:
        qs = LogEntry.objects.none()

    return object_list(
        request,
        queryset = qs,
        paginate_by = 20,
        allow_empty = True,
        template_name = 'admin_log.html',
        extra_context = ctx,
        )

@login_required
def mitglieder_csv( request, status = None ):
    response = HttpResponse( mimetype='text/csv' )
    response['Content-Disposition'] = 'attachment; filename=mitglieder.csv'

    writer = UnicodeWriter( response )
    writer.writerow( [ 
            'ID', 
            'VORNAME',
            'NACHNAME', 
            'GRADUIERUNG',
            'GRAD DATUM',
            'STATUS',
            'GEBURT',
            'STRASSE',
            'PLZ',
            'STADT',
            'EMAIL',
            'FON',
            'FAX',
            'MOBIL',
            'MITGLIED SEIT',
            'AUSTRITT AM',
            'VORSTAND',
            'TRAINER',
            'KIND',
            'BEKOMMT EMAILS',
            ] )

    if status is None:
        mitglieder = Mitglied.public_objects.all().exclude( status = 0 ).order_by( 'id' )
    else:
        mitglieder = Mitglied.public_objects.filter( status = status )

    for m in mitglieder:
        writer.writerow( [ 
                str( m.id ), 
                m.vorname, 
                m.nachname, 
                __get_graduierung( m ),
                __get_graduierung_datum( m ),
                m.get_status_display(), 
                __get_datum( m.geburt ),
                m.strasse, 
                m.plz, 
                m.stadt, 
                m.email ,
                m.fon ,
                m.fax ,
                m.mobil ,
                __get_datum( m.mitglied_seit ),
                __get_datum( m.austritt_am ),
                __get_bool( m.ist_vorstand ),
                __get_bool( m.ist_trainer ),
                __get_bool( m.ist_kind ),
                __get_bool( m.bekommt_emails ),
                ] )

    return response

def __get_graduierung( mitglied ):
    try:
        return mitglied.aktuelle_graduierung().get_graduierung_display()
    except:
        return ''

def __get_graduierung_datum( mitglied ):
    try:
        return __get_datum( mitglied.aktuelle_graduierung().datum )
    except:
        return ''

def __get_datum( datum ):
    try:
        return datum.strftime( '%d.%m.%Y' )
    except:
        return ''

def __get_bool( bool ):
    if bool:
        return 'J'
    else:
        return 'N'

@login_required
def members( request ):
    ctx = __get_sidebar( request )
    ctx['mitglieder'] = Mitglied.public_objects.all()

    return __create_response( request, ctx, 'mitglieder.html' )

@login_required
def mailinglist( request ):
    ctx = __get_sidebar( request )
    ctx['mitglieder'] = Mitglied.public_objects.all()

    return __create_response( request, ctx, 'mailverteiler.html' )

@login_required
def special_members( request ):
    ctx = __get_sidebar( request )
    ctx['mitglieder'] = Mitglied.public_objects.filter( status = 3 )

    return __create_response( request, ctx, 'mitglieder.html' )

@login_required
def active_members( request ):
    ctx = __get_sidebar( request )
    ctx['mitglieder'] = Mitglied.public_objects.filter( status = 1 )

    return __create_response( request, ctx, 'mitglieder.html' )

@login_required
def passive_members( request ):
    ctx = __get_sidebar( request )
    ctx['mitglieder'] = Mitglied.public_objects.filter( status = 2 )

    return __create_response( request, ctx, 'mitglieder.html' )

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

            if settings.SEND_MAIL_ON_LOGIN and not user.username == 'marcus':
                try:
                    subject = '%s hat sich eingeloggt' % user.first_name
                    message = '%s\n\nClient: %s\nIP: %s' % ( subject, request.META['HTTP_USER_AGENT'], request.META['REMOTE_ADDR'] )
                    mail_admins( subject, message, fail_silently = True )
                except:
                    pass

            next = request.REQUEST.get( 'next', settings.LOGIN_REDIRECT_URL )

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
    ctx['menu'] = 'links'

    ctx['links'] = Link.public_objects.all()
    ctx['kategorien'] = LinkKategorie.public_objects.all()

    return __create_response( request, ctx, 'links.html' )

def bilder( request ):
    ctx = __get_sidebar( request )
    ctx['menu'] = 'bilder'

    try:
        import gdata.photos.service
        username = 'ehemkemeier'
        ps = gdata.photos.service.PhotosService()
        albums = []
        for album in ps.GetFeed( '/data/feed/api/user/%s?kind=album&thumbsize=160&max-results=10' % ( username )  ).entry:
            photos = []
            for photo in ps.GetFeed( '/data/feed/api/user/%s/album/%s?kind=photo&thumbsize=48&max-results=10' % ( username, album.name.text ) ).entry:
                p = {
                    'url': photo.GetHtmlLink().href,
                    'thumb_url': photo.media.thumbnail[0].url,
                    'thumb_height': photo.media.thumbnail[0].height,
                    'thumb_width': photo.media.thumbnail[0].width,
                    }

                if photo.summary.text:
                    p['title'] = photo.summary.text
                else:
                    p['title'] = photo.title.text

                photos.append( p )

            a = {
                'title': album.title.text,
                'name': album.name.text,
                'url': album.GetHtmlLink().href,
                'numcomments': album.commentCount.text,
                'numphotos': album.numphotos.text,
                'thumb_url': album.media.thumbnail[0].url,
                'thumb_height': album.media.thumbnail[0].height,
                'thumb_width': album.media.thumbnail[0].width,
                'photos': photos,
                }

            try:
                a['timestamp'] = album.timestamp.text[:10]
            except:
                pass

            albums.append( a )
            
        ctx['username'] = username
        ctx['albums'] = albums
    except Exception, ex:
        mail_admins( 'Picasa error',  ex, fail_silently = False )
        ctx['picasa_error'] = True
        #raise ex

    return __create_response( request, ctx, 'bilder.html' )

def downloads( request ):
    ctx = __get_sidebar( request )
    ctx['menu'] = 'downloads'
    ctx['downloads'] = Download.public_objects.all()

    return __create_response( request, ctx, 'downloads.html' )

def news( request, bid = None ):
    ctx = __get_sidebar( request )
    ctx['menu'] = 'news'

    if bid:
        all_news = News.public_objects.all()
        beitrag = get_object_or_404( News.public_objects, id = bid )
        ctx['beitrag'] = beitrag
        ctx['anzahl'] = all_news.count()
        try:
            heute = date.today()
            ctx['next'] = beitrag.get_previous_by_beginn( public = True, beginn__lte = heute, ende__isnull = True )
            ctx['previous'] = beitrag.get_next_by_beginn( public = True, beginn__lte = heute, ende__isnull = True )
        except:
            pass
        return __create_response( request, ctx, 'news.html' )
    else:
        return object_list(
            request,
            queryset = News.public_objects.all(),
            paginate_by = 20,
            allow_empty = True,
            template_name = 'news_list.html',
            extra_context = ctx,
            )

def video( request, vid = None ):
    ctx = __get_sidebar( request )
    ctx['menu'] = 'videos'

    import youtube
    username = 'eckido'
    client = youtube.YouTubeClient( 'gmsnG0W2bTA' )
    ctx['videos'] = client.list_by_user( username, page = 1, per_page = 10 )
    ctx['username'] = username

    if vid:
        video = client.get_details( vid )
        if video:
            ctx['vid'] = vid
            ctx['watch'] = video

#    import gdata.youtube.service
#    ys = gdata.youtube.service.YouTubeService()
#    videos = []
#    if vid:
#        feed = None
#    else:
#        feed = ys.GetYouTubeVideoFeed( 'http://gdata.youtube.com/feeds/api/videos?author=%s&orderby=published&max-results=10' % username )
#
#    for video in feed.entry:
#        v = {
#            'id': video.id.text,
#            'title': video.media.title.text,
#            'description': video.media.description.text,
#            'length': video.media.duration.seconds,
#            'view_count': video.statistics.view_count,
#            'author': username,
#            'thumbnail_url': video.media.thumbnail[0].url,
#            'xml': video,
#            }
#        videos.append( v )
#        
#    ctx['videos'] = videos
    
    return __create_response( request, ctx, 'videos.html' )

def termin( request, tid = None ):
    ctx = __get_sidebar( request )

    if tid:
        ctx['termin'] = get_object_or_404( Termin.public_objects, id = tid )
        return __create_response( request, ctx, 'termin.html' )
    else:
        return object_list(
            request,
            queryset = Termin.public_objects.all(),
            paginate_by = 20,
            allow_empty = True,
            template_name = 'termine_list.html',
            extra_context = ctx,
            )

def set_lang( request, code = settings.LANGUAGE_CODE ):
    if code in dict(settings.LANGUAGES).keys():
        request.session['django_language'] = code
    return set_language( request )

def __create_response( request, context = {}, template_name = 'base.html' ):
    return render_to_response(
        template_name,
        context,
        context_instance = RequestContext( request ),
    )
