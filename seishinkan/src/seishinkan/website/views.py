#-*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from django import get_version
from django.contrib.admin.models import LogEntry
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import mail_admins, send_mail, send_mass_mail, EmailMessage, SMTPConnection
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.i18n import set_language
from seishinkan import settings
from seishinkan.links.models import Link, LinkKategorie
from seishinkan.members.models import *
from seishinkan.news.models import News
from seishinkan.utils import UnicodeWriter, get_next_month
from seishinkan.website.forms import LoginForm, KontaktForm
from seishinkan.website.models import *
import captcha
import django
import locale, os, platform, re, sys
import pyExcelerator as xl

try:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute( "SELECT version()" )
    version = cursor.fetchone()[0]
    if version.lower().startswith( 'postgresql' ):
        db_version = version[:version.find( ' ', 12 )]
        db_link = 'http://www.postgresql.org/'
    else:
        db_version = 'MySQL %s' % version
        db_link = 'http://www.mysql.de/'
except:
    db_version = ''
    db_link = ''

def __get_sidebar( request ):
    heute = int( datetime.today().strftime( '%w' ) )

    ctx = { }
    ctx['sidebar'] = True
    ctx['seiten'] = Seite.public_objects.filter( parent__isnull = True ).order_by( 'position' )
    ctx['language'] = request.session.get( 'django_language', 'de' )
    ctx['training_heute'] = TrainingManager().get_einheiten_pro_tag( heute )
    ctx['termine_heute'] = Termin.public_objects.current()
    ctx['training_aktuell'] = TrainingAktuell.public_objects.get_aktuelle_meldungen()
    ctx['homepage'] = Seite.public_objects.get_homepage()

    ctx['os_version'] = platform.platform( 1, 1 )
    ctx['python_version'] = '%s.%s.%s %s (%s)' % sys.version_info
    ctx['db_version'] = db_version
    ctx['db_link'] = db_link
    ctx['django_version'] = get_version()

    try:
        ctx['wochentag'] = Wochentag.objects.get( id = heute )
        ctx['path'] = request.path
        ctx['host'] = request.META['HTTP_HOST']
    except:
        pass

    if request.user.is_authenticated():
        ctx['users'] = User.objects.all().order_by( '-last_login' )
        ctx['nonpublic_sites'] = Seite.objects.filter( public = False ).order_by( 'position' )

    return ctx

def index( request, sid = 1 ):
    ctx = __get_sidebar( request )

    seite = get_object_or_404( Seite.objects, id = sid )
    if not seite.public and request.user.is_anonymous():
        raise Http404
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
        
    if seite.show_jugend:
        jugendtraining = Training.objects.filter( public = True, art__ist_jugendtraining = True )
        if jugendtraining and jugendtraining.count() > 0:
            ctx['jugendtraining_liste'] = jugendtraining
            ctx['jugendtraining'] = jugendtraining[0].art
        
    return __create_response( request, ctx )

def my_404( request ):
    ctx = __get_sidebar( request )
    ctx['request_path'] = request.get_full_path()
    if settings.SEND_BROKEN_LINK_EMAILS:
        subject = 'Broken Link: %s' % request.get_full_path()
        message = '%s' % ( request )
        mail_admins( subject, message, fail_silently = True )
    return __create_response( request, ctx, template_name = '404.html' )

def dynamic_url( request, sitename = '' ):
    if not sitename or sitename.strip() == '':
        return index( request )

    seite = get_object_or_404( Seite.objects, url__iexact = sitename )
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

            marcus = User.objects.get( username__iexact = 'marcus' )
            ecki = User.objects.get( username__iexact = 'ecki' )
            bert = User.objects.get( username__iexact = 'bert' )
            ralf = User.objects.get( username__iexact = 'ralf' )

            to_users = [ ecki, marcus ]
            to_list = []
            for user in to_users:
                if user.email:
                    to_list.append( user.email )

            name = form.data['name']

            if name:
                from_email = '%s <%s>' % ( name, form.data['email'] )
            else:
                from_email = form.data['email']

            subject = form.data['subject']
            message = form.data['message']

            # Wenn gewÅ¸nscht, Kopie an den Absender...
            if form.data.get( 'copy_to_me', False ):
                to_list.append( from_email )

            # In Datenbank speichern...
            kontakt = Kontakt( sender = from_email, betreff = subject, nachricht = message )
            kontakt.captcha = request.POST['recaptcha_response_field']
            kontakt.to = to_list
            kontakt.save()

            # Email senden
            subject = settings.EMAIL_SUBJECT_PREFIX + subject
            message = '%s\n\n%s' % ( message, settings.EMAIL_MESSAGE_POSTFIX )
#            mail = EmailMessage( subject = subject, body = message, to = to_list, bcc = [], headers = { 'Reply-To': from_email } )
#            mail.send()

            # Connection zum Strato SMTP Server
            con = SMTPConnection()
            con.host = settings.STRATO_EMAIL_HOST
            con.username = settings.STRATO_EMAIL_HOST_USER
            con.password = settings.STRATO_EMAIL_HOST_PASSWORD
            con.use_tls = settings.STRATO_EMAIL_USE_TLS

            # Email zusammenbauen und verschicken
            email = EmailMessage()
            email.subject = subject
            email.body = message
            email.from_email = from_email
            # EmpfÅ‰ngerliste in Blindkopie (bcc)
            email.bcc = to_list
            email.headers = { 'Reply-To': from_email }
            email.connection = con
            email.send()

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
def mitglieder_xls( request, status = None ):
    if not ist_vorstand( request.user ):
        return __create_response( request, ctx, 'keine_berechtigung.html' )

    workbook = xl.Workbook()
    sheet = workbook.add_sheet( 'Mitglieder' )
    header_font = xl.Font()
    header_font.bold = True
    header_style = xl.XFStyle()
    header_style.font = header_font
    
    if status is None:
        mitglieder = Mitglied.public_objects.all().exclude( status = 0 ).order_by( 'id' )
    else:
        mitglieder = Mitglied.public_objects.filter( status = status )

    for y, header in enumerate( __get_headers() ):
        sheet.write( 0, y, header, header_style )

    for x, mitglied in enumerate( mitglieder ):
        col = 0
        for y, content in enumerate( __get_content( mitglied ) ):
            sheet.write( x + 1, y, content )
            col = y
            
    filename = 'mitglieder-%s.xls' % datetime.now().strftime( '%Y%m%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype = 'application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@login_required
def mitglieder_csv( request, status = None ):
    if not ist_vorstand( request.user ):
        return __create_response( request, ctx, 'keine_berechtigung.html' )

    response = HttpResponse( mimetype = 'text/csv' )
    response['Content-Disposition'] = 'attachment; filename=mitglieder.csv'

    writer = UnicodeWriter( response )
    writer.writerow( __get_headers() )

    if status is None:
        mitglieder = Mitglied.public_objects.all().exclude( status = 0 ).order_by( 'id' )
    else:
        mitglieder = Mitglied.public_objects.filter( status = status )

    for m in mitglieder:
        writer.writerow( __get_content( m ) )

    return response

def __get_headers():
    return [ 'M-ID', 'VORNAME', 'NACHNAME', 'GRADUIERUNG', 'GRAD DATUM', 'STATUS', 'GEBURT', 'STRASSE', 'PLZ', 'STADT', 'LAND', 'EMAIL', 'FON', 'FAX', 'MOBIL', 'MITGLIED SEIT', 'AUSTRITT AM', 'VORSTAND', 'TRAINER', 'KIND', 'BEKOMMT EMAILS' ]

def __get_content( m ):
    return [
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
        unicode( m.land ),
        m.email,
        m.fon,
        m.fax,
        m.mobil,
        __get_datum( m.mitglied_seit ),
        __get_datum( m.austritt_am ),
        __get_bool( m.ist_vorstand ),
        __get_bool( m.ist_trainer ),
        __get_bool( m.ist_kind ),
        __get_bool( m.bekommt_emails ),
        ]

def __get_graduierung( mitglied ):
    if mitglied is None or mitglied.graduierung is None:
        return ''
    try:
        return mitglied.aktuelle_graduierung().get_graduierung_display()
    except:
        return ''

def __get_graduierung_datum( mitglied ):
    try:
        return __get_datum( mitglied.graduierung_datum )
    except:
        return ''

def __get_datum( datum ):
    if datum is None:
        return ''
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
def trainerliste_xls( request, year, month ):
    try:
        year = int( year )
        month = int( month )
    except:
        nm = get_next_month()
        year = nm.year
        month = nm.month

    locale.setlocale( locale.LC_ALL, 'de_DE' )

    datum = date( year, month, 1 )
    workbook = xl.Workbook()
    sheet = workbook.add_sheet( 'Trainerliste %s' % datum.strftime( '%Y-%m' ) )
    sheet.set_print_grid( True )
    sheet.set_portrait( False )
    sheet.set_fit_num_pages( 1 )
    sheet.set_header_str( '' )

    font = xl.Font()
    font.name = 'Bitstream Vera Sans'
    center = xl.Alignment()
    center.horz = xl.Alignment.HORZ_CENTER
    center.vert = xl.Alignment.VERT_CENTER
    left = xl.Alignment()
    left.horz = xl.Alignment.HORZ_LEFT
    left.vert = xl.Alignment.VERT_CENTER
    orient = xl.Alignment()
    orient.orie = xl.Alignment.ORIENTATION_90_CC

    style = xl.XFStyle()
    style.font = font
    style.alignment = center

    fb = xl.Font()
    fb.height = font.height * 2
    big = xl.XFStyle()
    big.font = fb
    big.alignment = left

    sheet.row( 0 ).set_style( style )
    sheet.write( 0, 0, datum.strftime( '%B %Y' ), big )

    style.alignment = center
    COLX = 6
    i = COLX
    alle_trainer =  Mitglied.public_objects.get_trainer().order_by('-graduierung', 'graduierung_datum')
    anzahl_trainer = len ( alle_trainer )
    for t in alle_trainer:
        sheet.write( 0, i, t.vorname, style )
        i += 1
    
    einTag = timedelta( days = 1 )
    style.alignment = center
    row = 1
    while month == datum.month:
        einheitenProTag = TrainingManager().get_einheiten_pro_tag( int( datum.strftime( '%w' ) ) )
        for training in einheitenProTag:
            sheet.row( row ).set_style( style )
            style.alignment = center
            sheet.write( row, 0, row, style )
            sheet.write( row, 1, datum.strftime( '%d.%m.%Y' ), style )
            style.alignment = center
            sheet.write( row, 2, training.wochentag.get_name()[:2], style )
            style.alignment = center
            sheet.write( row, 3, training.von.strftime( '%H:%M' ), style )
            sheet.write( row, 4, training.bis.strftime( '%H:%M' ), style )
            style.alignment = left
            sheet.write( row, 5, training.art.get_name(), style )

            style.alignment = center
            for i in range( anzahl_trainer ):
                sheet.write( row, i+COLX, '', style )
            
            x1 = chr( ord( 'A' ) + COLX ) + str( row + 1 )
            x2 = chr( ord( 'A' ) + COLX + anzahl_trainer - 1 ) + str( row + 1 )
            sheet.write( row, COLX+anzahl_trainer, xl.Formula( 'COUNTA(%s:%s)' % ( x1, x2 ) ), style )
                
            row += 1
        datum += einTag

    row += 1
    fon = ''
    for t in alle_trainer:
        if t.mobil:
            fon += '%s: %s, ' % ( t.vorname, t.mobil )
    f2 = xl.Font()
    f2.height = font.height * 3 / 4
    style.alignment = left
    style.font = f2
    sheet.write( row, 0, fon, style )
    
    sheet.row(0).height = 256 * 3

    sheet.col(0).width = 256 * 5
    sheet.col(1).width = 256 * 12
    sheet.col(2).width = 256 * 5
    sheet.col(3).width = 256 * 7
    sheet.col(4).width = 256 * 7
    sheet.col(5).width = 256 * 18
    for i in range( anzahl_trainer ):
        sheet.col(i+COLX).width = 256 * 12
    sheet.col(COLX + anzahl_trainer).width = 256 * 5

    filename = 'trainerliste-%s.xls' % datetime.now().strftime( '%Y-%m-%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype = 'application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@login_required
def teilnehmerliste_xls( request, year, month ):
    try:
        year = int( year )
        month = int( month )
    except:
        nm = get_next_month()
        year = nm.year
        month = nm.month

    locale.setlocale( locale.LC_ALL, 'de_DE' )

    datum = date( year, month, 1 )
    workbook = xl.Workbook()
    sheet = workbook.add_sheet( 'Teilnehmerliste %s' % datum.strftime( '%Y-%m' ) )
    sheet.set_print_grid( True )
    sheet.set_portrait( False )
    sheet.set_fit_num_pages( 2 )
    sheet.set_fit_width_to_pages( 1 )
    sheet.set_fit_height_to_pages( 1 )
    sheet.set_header_str( '' )

    font = xl.Font()
    font.name = 'Bitstream Vera Sans'
    fb = xl.Font()
    fb.bold = True
    center = xl.Alignment()
    center.horz = xl.Alignment.HORZ_CENTER
    center.vert = xl.Alignment.VERT_CENTER
    left = xl.Alignment()
    left.horz = xl.Alignment.HORZ_LEFT
    left.vert = xl.Alignment.VERT_CENTER
    orient = xl.Alignment()
    orient.orie = xl.Alignment.ORIENTATION_90_CC

    style = xl.XFStyle()
    style.font = fb

    style.alignment = left
    sheet.write( 0, 0, datum.strftime( '%B %Y' ), style )
    sheet.write( 1, 0, 'Vorname', style )
    sheet.write( 1, 1, 'Name', style )

    style.alignment = center
    style.font = font

    wochentage = TrainingManager().get_wochentage_ids()
    i = 2
    for tag in range( 1, 32 ):
        try:
            datum = date( year, month, tag )
            wochentag = int( datum.strftime( '%w' ) )
            if wochentag in wochentage:
                sheet.write( 0, i, datum.strftime( '%a' ), style )
                sheet.write( 1, i, datum.strftime( '%d.' ), style )
                i += 1
        except:
            i += 1

    erwachsene = Mitglied.public_objects.get_nicht_passive_mitglieder().filter( ist_kind = False )
    anzahl_erwachsene = len( erwachsene )
    for i, erwachsener in enumerate( erwachsene):
        style.alignment = left
        row = i + 2
        sheet.write( row, 0, erwachsener.vorname, style )
        sheet.write( row, 1, erwachsener.nachname, style )

    style.alignment = left
    style.font = fb

    row = anzahl_erwachsene + 4
    style.alignment = left
    sheet.write( row, 0, 'Kindertraining', style )
    sheet.write( row + 1, 0, 'Vorname', style )
    sheet.write( row + 1, 1, 'Name', style )

    style.alignment = center
    style.font = font

    wochentage = TrainingManager().get_kinder_wochentage_ids()
    i = 2
    for tag in range( 1, 32 ):
        try:
            datum = date( year, month, tag )
            wochentag = int( datum.strftime( '%w' ) )
            if wochentag in wochentage:
                sheet.write( row, i, datum.strftime( '%a' ), style )
                sheet.write( row + 1, i, datum.strftime( '%d.' ), style )
                i += 1
        except:
            i += 1

    kinder = Mitglied.public_objects.get_nicht_passive_mitglieder().filter( ist_kind = True )
    for i, kind in enumerate( kinder):
        style.alignment = left
        row = i + anzahl_erwachsene + 6
        sheet.write( row, 0, kind.vorname, style )
        sheet.write( row, 1, kind.nachname, style )

    sheet.col(0).width = 256 * 20
    sheet.col(1).width = 256 * 20
    for i in range( 31 ):
        sheet.col(i + 2).width = 256 * 5

    filename = 'teilnehmerliste-%s.xls' % datetime.now().strftime( '%Y-%m-%d-%H%M%S' )
    workbook.save( 'tmp/' + filename )
    response = HttpResponse( open( 'tmp/' + filename, 'r' ).read(), mimetype = 'application/ms-excel' )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@login_required
def mitgliederlisten( request ):
    ctx = __get_sidebar( request )

    if not ist_vorstand( request.user ):
        return __create_response( request, ctx, 'keine_berechtigung.html' )

    ctx['menu'] = 'mitgliederlisten'
    ctx['status'] = STATUS
    ctx['months'] = [ date.today(), get_next_month() ]

    return __create_response( request, ctx, 'mitglieder.html' )

@login_required
def graduierungen( request ):
    ctx = __get_sidebar( request )

    if not ist_vorstand( request.user ):
        return __create_response( request, ctx, 'keine_berechtigung.html' )

    ctx['menu'] = 'graduierungen'

    ctx['vorschlaege'] = Graduierung.public_objects.filter( vorschlag = True )
    ctx['mitglieder'] = Mitglied.public_objects.get_mitglieder().order_by( '-graduierung', 'graduierung_datum', 'vorname', 'nachname' )
#    ctx['vorschlaege'] = Mitglied.public_objects.get_mitglieder().filter( vorschlag = True ).order_by( '-graduierung', 'graduierung_datum', 'vorname', 'nachname' )

    return __create_response( request, ctx, 'graduierungen.html' )

@login_required
def mailinglist( request ):
    ctx = __get_sidebar( request )

    if not ist_vorstand( request.user ):
        return __create_response( request, ctx, 'keine_berechtigung.html' )

    ctx['menu'] = 'emailverteiler'
    ctx['redakteure'] = User.objects.filter( email__isnull = False, email__contains = '@', is_active = True, is_staff = True ).order_by( 'first_name', 'last_name', 'username' )
    ctx['vorstand'] = Mitglied.public_objects.get_mitglieder_mit_email().filter( ist_vorstand = True )
    ctx['trainer'] = Mitglied.public_objects.get_mitglieder_mit_email().filter( ist_trainer = True )
    ctx['mit_mail'] = Mitglied.public_objects.get_mitglieder_mit_email()
    ctx['ohne_mail'] = Mitglied.public_objects.get_mitglieder_ohne_email()

    return __create_response( request, ctx, 'mailverteiler.html' )

@login_required
def permissions( request ):
    ctx = __get_sidebar( request )

    if not ist_vorstand( request.user ):
        return __create_response( request, ctx, 'keine_berechtigung.html' )

    ctx['users'] = User.objects.all().order_by( 'first_name', 'last_name' )
    ctx['groups'] = Group.objects.all()

    return __create_response( request, ctx, 'berechtigungen.html' )

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
                    subject = '%s hat sich eingeloggt (%s)' % ( user.first_name, datetime.now().strftime( '%d.%m.%Y %H:%M' ) )
                    message = '%s\n\nClient: %s\nIP: %s\n\nhttp://www.aikido-dojo-seishinkan.de/' % ( subject, request.META['HTTP_USER_AGENT'], request.META['REMOTE_ADDR'] )
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
        for album in ps.GetFeed( '/data/feed/api/user/%s?kind=album&thumbsize=160&max-results=10' % ( username ) ).entry:
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
        mail_admins( 'Picasa error', ex, fail_silently = False )
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

    try:
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
    except:
        ctx['vid'] = vid
        ctx['youtube_error'] = True

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
    if code in dict( settings.LANGUAGES ).keys():
        request.session['django_language'] = code
    return set_language( request )

def __create_response( request, context = {}, template_name = 'base.html' ):
    return render_to_response( 
        template_name,
        context,
        context_instance = RequestContext( request ),
    )

def ist_vorstand( user ):
    try:
        return user.has_module_perms( 'members' )
    except:
        return False
