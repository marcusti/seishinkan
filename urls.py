from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from seishinkan.website.feeds import NewsFeed, TerminFeed

admin.autodiscover()

feeds = {
  'termine': TerminFeed,
  'news': NewsFeed,
}

urlpatterns = patterns('',
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^verwaltung/doc/', include('django.contrib.admindocs.urls')),
    (r'^verwaltung/', include(admin.site.urls)),
    (r'^feed/termine/$', TerminFeed()),
    (r'^feed/news/$', NewsFeed()),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
  )

# Simple Generic Views
urlpatterns += patterns('django.views.generic.simple',
    (r'^accounts/$', 'redirect_to', {'url': '/'}),
)

# Seishinkan Website Views
urlpatterns += patterns('seishinkan.website.views',
    (r'^$', 'index'),
    (r'^login/$', 'seishinkan_login'),
    (r'^lang/(.*)/$', 'set_lang'),
    (r'^logout/$', 'seishinkan_logout'),
    (r'^seite/(\d+)/$', 'index'),
    (r'^links/$', 'links'),
    (r'^kontakt/$', 'kontakt'),
    (r'^news/$', 'news'),
    (r'^news/(\d+)/$', 'news'),
    (r'^news/archiv/$', 'news'),
    (r'^termin/$', 'termin'),
    (r'^termin/(\d+)/$', 'termin'),
    (r'^termin/archiv/$', 'termin'),
    (r'^termine/$', 'termin'),
    (r'^termine/archiv/$', 'termin'),
    (r'^impressum/$', 'impressum'),
    (r'^info/$', 'info'),
    (r'^sysinfo/$', 'sysinfo'),
    (r'^videos/$', 'video'),
    (r'^bilder/$', 'picasa_albums'),
    (r'^bilder/(.+)/$', 'picasa_photos'),
    (r'^downloads/$', 'downloads'),
    # (r'^videos/(.+)/$', 'video'),
    (r'^email/$', 'mailinglist'),
    (r'^log/$', 'admin_log'),
    (r'^permissions/$', 'permissions'),
    (r'^graduierungen/$', 'graduierungen'),
    (r'^mitglieder/$', 'mitgliederlisten'),
    (r'^mitglieder/csv/$', 'mitglieder_csv'),
    (r'^mitglieder/csv/(\d+)/$', 'mitglieder_csv'),
    (r'^mitglieder/xls/$', 'mitglieder_xls'),
    (r'^mitglieder/xls/(\d+)/$', 'mitglieder_xls'),
    (r'^trainerliste/(\d+)/(\d+)/$', 'trainerliste_xls'),
    (r'^teilnehmerliste/(\d+)/(\d+)/$', 'teilnehmerliste_xls'),

    # dynamic_url muss am Ende stehen
    (r'^(.+)/$', 'dynamic_url'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

handler404 = 'seishinkan.website.views.my_404'
