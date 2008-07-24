from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns( '',
    # Example:
    # (r'^seishinkan/', include('seishinkan.foo.urls')),

    # Uncomment this for admin:
    ( r'^i18n/', include( 'django.conf.urls.i18n' ) ),
    ( r'^verwaltung/doc/', include( 'django.contrib.admindocs.urls' ) ),
    ( r'^verwaltung/(.*)', admin.site.root ),
    #( r'^kontakt/', include( 'contact_form.urls' ) ),
    #( r'^logout/$', 'django.contrib.auth.views.logout' ),
 )

# Simple Generic Views
urlpatterns += patterns( 'django.views.generic.simple',
#    ( r'^seishinkan/$', 'direct_to_template', {'template': 'base.html'} ),
    ( r'^accounts/$', 'redirect_to', {'url': '/'} ),
 )

urlpatterns += patterns( 'seishinkan.website.views',
    ( r'^$', 'index' ),
    ( r'^login/$', 'seishinkan_login' ),
    ( r'^logout/$', 'seishinkan_logout' ),
    ( r'^seite/(\d+)/$', 'index' ),
    ( r'^links/$', 'links' ),
    ( r'^kontakt/$', 'kontakt' ),
    ( r'^news/$', 'news' ),
    ( r'^news/(\d+)/$', 'news' ),
    ( r'^news/archiv/$', 'news_archiv' ),
    ( r'^termin/(\d+)/$', 'termin' ),
    ( r'^termin/archiv/$', 'termine_archiv' ),
    ( r'^impressum/$', 'impressum' ),
    ( r'^info/$', 'info' ),
    ( r'^sysinfo/$', 'sysinfo' ),
    ( r'^video/$', 'video' ),
    ( r'^bilder/$', 'bilder' ),
    ( r'^downloads/$', 'downloads' ),
    ( r'^video/(.+)/$', 'video' ),
    ( r'^(.+)/$', 'dynamic_url' ),
 )

if settings.DEBUG:
    urlpatterns += patterns( '',
        ( r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/max/eclipse/workspace/seishinkan/htdocs/static'} ),
     )

