from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns( '',
    ( r'^i18n/', include( 'django.conf.urls.i18n' ) ),
    ( r'^verwaltung/doc/', include( 'django.contrib.admindocs.urls' ) ),
    ( r'^verwaltung/(.*)', admin.site.root ),
 )

# Simple Generic Views
urlpatterns += patterns( 'django.views.generic.simple',
    ( r'^accounts/$', 'redirect_to', {'url': '/'} ),
 )

# Seishinkan Website Views
urlpatterns += patterns( 'seishinkan.website.views',
    ( r'^$', 'index' ),
    ( r'^login/$', 'seishinkan_login' ),
    ( r'^lang/(.*)/$', 'set_lang' ),
    ( r'^logout/$', 'seishinkan_logout' ),
    ( r'^seite/(\d+)/$', 'index' ),
    ( r'^links/$', 'links' ),
    ( r'^kontakt/$', 'kontakt' ),
    ( r'^news/$', 'news' ),
    ( r'^news/(\d+)/$', 'news' ),
    ( r'^news/archiv/$', 'news' ),
    ( r'^termin/$', 'termin' ),
    ( r'^termin/(\d+)/$', 'termin' ),
    ( r'^termin/archiv/$', 'termin' ),
    ( r'^termine/$', 'termin' ),
    ( r'^termine/archiv/$', 'termin' ),
    ( r'^impressum/$', 'impressum' ),
    ( r'^info/$', 'info' ),
    ( r'^sysinfo/$', 'sysinfo' ),
    ( r'^video/$', 'video' ),
    ( r'^bilder/$', 'bilder' ),
    ( r'^downloads/$', 'downloads' ),
    ( r'^video/(.+)/$', 'video' ),
    ( r'^email/$', 'mailinglist' ),
    ( r'^log/$', 'admin_log' ),
    ( r'^mitglieder/$', 'mitglieder' ),
    ( r'^mitglieder/csv/$', 'mitglieder_csv' ),
    ( r'^mitglieder/csv/(\d+)/$', 'mitglieder_csv' ),
    ( r'^mitglieder/xls/$', 'mitglieder_xls' ),
    ( r'^mitglieder/xls/(\d+)/$', 'mitglieder_xls' ),

    # dynamic_url muss am Ende stehen
    ( r'^(.+)/$', 'dynamic_url' ),
 )

if settings.DEBUG:
    urlpatterns += patterns( '',
        ( r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/max/eclipse/workspace/seishinkan/htdocs/static'} ),
     )
