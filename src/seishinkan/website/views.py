from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from seishinkan import settings
from seishinkan.website.models import Artikel, Seite, Termin, TrainingManager, Wochentag
from seishinkan.news.models import News
from seishinkan.links.models import Link, LinkKategorie

def __get_sidebar( request ):
    if Artikel.objects.all().count() == 0:
        import initialData
        #initialData.Import()

    c = { }
    c['seiten'] = Seite.public_objects.filter( parent__isnull = True )
    c['language'] = request.session.get( 'django_language', 'de' )
    c['termine'] = Termin.public_objects.current()
    c['alle_termine'] = Termin.public_objects.all()
    c['beitraege'] = News.public_objects.all()
    return c

def index( request, sid = 1 ):
    c = __get_sidebar( request )
    seite = get_object_or_404( Seite.public_objects, id = sid )
    c['seite'] = seite
    c['artikel'] = Artikel.public_objects.get_by_category( sid )
    if seite.show_training:
        c['wochenplan'] = TrainingManager().get_wochenplan()
        c['wochentage'] = TrainingManager().get_wochentage()

    return render_to_response(
        'base.html',
        c,
        context_instance = RequestContext( request ),
    )

def links( request ):
    c = __get_sidebar( request )
    c['links'] = Link.public_objects.all()
    c['kategorien'] = LinkKategorie.objects.all()

    return render_to_response(
        'links.html',
        c,
        context_instance = RequestContext( request ),
    )

def news( request, bid = None ):
    c = __get_sidebar( request )
    c['beitraege'] = News.public_objects.all()
    if bid:
        c['beitrag'] = get_object_or_404( News.public_objects, id = bid )

    return render_to_response(
        'news.html',
        c,
        context_instance = RequestContext( request ),
    )

def news_archiv( request ):
    c = __get_sidebar( request )

    return render_to_response(
        'news_list.html',
        c,
        context_instance = RequestContext( request ),
    )

def termine_archiv( request ):
    c = __get_sidebar( request )

    return render_to_response(
        'termine_list.html',
        c,
        context_instance = RequestContext( request ),
    )

def termin( request, tid = None ):
    c = __get_sidebar( request )

    if tid:
        c['termin'] = get_object_or_404( Termin.public_objects, id = tid )

    return render_to_response(
        'termin.html',
        c,
        context_instance = RequestContext( request ),
    )

#    return object_list(
#        request,
#        queryset = Seite.objects.filter( public = True ),
#        template_name = 'base.html',
#    )

