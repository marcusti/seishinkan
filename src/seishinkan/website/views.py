import os
from datetime import date, datetime
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template, redirect_to
from seishinkan import settings
from seishinkan.website.forms import LoginForm
from seishinkan.links.models import Link, LinkKategorie
from seishinkan.news.models import News
from seishinkan.website.models import Artikel, Bild, Seite, Termin, TrainingManager, Trainingsart, Wochentag

def __get_sidebar( request ):
    heute = int( datetime.today().strftime( '%w' ) )

    ctx = { }
    ctx['sidebar'] = True
    ctx['seiten'] = Seite.public_objects.filter( parent__isnull = True )
    ctx['language'] = request.session.get( 'django_language', 'de' )
    ctx['termine'] = Termin.public_objects.current()
    ctx['alle_termine'] = Termin.public_objects.all()
    ctx['beitraege'] = News.public_objects.all()
    ctx['training_heute'] = TrainingManager().get_einheiten_pro_tag( heute )
    ctx['wochentag'] = get_object_or_404( Wochentag.objects, id = heute )

    if request.user.is_authenticated():
        ctx['users'] = User.objects.all().order_by( '-last_login' )
        
    return ctx

def index( request, sid = 1 ):
    ctx = __get_sidebar( request )

    seite = get_object_or_404( Seite.public_objects, id = sid )
    ctx['seite'] = seite
    ctx['artikel'] = Artikel.public_objects.get_by_category( sid )

    if seite.show_training:
        ctx['wochenplan'] = TrainingManager().get_wochenplan()
        ctx['wochentage'] = TrainingManager().get_wochentage()
        ctx['trainingsarten'] = Trainingsart.objects.filter( public = True )

    return __create_response( request, ctx )

def info( request, sid = 1 ):
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

    return __create_response( request, ctx, 'info.html' )

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
    ctx['kategorien'] = LinkKategorie.objects.all()

    return __create_response( request, ctx, 'links.html' )

def news( request, bid = None ):
    ctx = __get_sidebar( request )
    ctx['beitraege'] = News.public_objects.all()
    if bid:
        ctx['beitrag'] = get_object_or_404( News.public_objects, id = bid )

    return __create_response( request, ctx, 'news.html' )

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

def news_archiv( request ):
    ctx = __get_sidebar( request )
    return __create_response( request, ctx, 'news_list.html' )

def termine_archiv( request ):
    ctx = __get_sidebar( request )
    return __create_response( request, ctx, 'termine_list.html' )

def termin( request, tid = None ):
    ctx = __get_sidebar( request )

    if tid:
        ctx['termin'] = get_object_or_404( Termin.public_objects, id = tid )

    return __create_response( request, ctx, 'termin.html' )

def __create_response( request, context = {}, template_name = 'base.html' ):
    return render_to_response(
        template_name,
        context,
        context_instance = RequestContext( request ),
    )
