from django.conf.urls.defaults import *

urlpatterns = patterns( '',
    # Example:
    # (r'^seishinkan/', include('seishinkan.foo.urls')),

    # Uncomment this for admin:
    ( r'^i18n/', include( 'django.conf.urls.i18n' ) ),
    ( r'^admin/', include( 'django.contrib.admin.urls' ) ),
)

# Simple Generic Views
urlpatterns += patterns( 'django.views.generic.simple',
#    ( r'^seishinkan/$', 'direct_to_template', {'template': 'base.html'} ),
    ( r'^accounts/$',  'redirect_to', {'url': '/'} ),
)

urlpatterns += patterns( 'seishinkan.website.views',
    ( r'^$', 'index' ),
    ( r'^seite/(\d+)/$', 'index' ),
    ( r'^beitrag/$', 'news' ),
    ( r'^beitrag/(\d+)/$', 'news' ),
)


