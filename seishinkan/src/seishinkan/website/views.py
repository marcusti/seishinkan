from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from seishinkan import settings
from seishinkan.website.models import Artikel, Beitrag, Kategorie, Konfiguration, Termin, TrainingManager, Wochentag

def __get_sidebar( request ):
    if Artikel.objects.all().count() == 0:
        import initialData
        initialData.Import()

    c = { }
    c['kategorien'] = Kategorie.public_objects.filter( parent__isnull = True )
    c['language'] = request.session.get( 'django_language', 'de' )
    c['termine'] = Termin.public_objects.current()
    c['beitraege'] = Beitrag.public_objects.all()
    return c

def index( request, kid = 1 ):
    c = __get_sidebar( request )
    konf = Konfiguration.objects.get( id = 1 )
    kategorie = get_object_or_404( Kategorie.public_objects, id = kid )
    c['kategorie'] = kategorie
    c['artikel'] = Artikel.public_objects.get_by_category( kid )
    if konf.trainingskategorie == kategorie:
        c['wochenplan'] = TrainingManager().get_wochenplan()
        c['wochentage'] = TrainingManager().get_wochentage()

    return render_to_response(
        'base.html',
        c,
        context_instance = RequestContext( request ),
    )

def news( request, bid = None ):
    c = __get_sidebar( request )
    c['beitraege'] = Beitrag.public_objects.all()
    if bid:
        c['beitrag'] = get_object_or_404( Beitrag.public_objects, id = bid )

    return render_to_response(
        'news.html',
        c,
        context_instance = RequestContext( request ),
    )

#    return object_list(
#        request,
#        queryset = Kategorie.objects.filter( public = True ),
#        template_name = 'base.html',
#    )

