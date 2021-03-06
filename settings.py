#-*- coding: utf-8 -*-
# Django settings for seishinkan project.

EMAIL_SUBJECT_PREFIX = '[seishinkan.de] '
EMAIL_MESSAGE_POSTFIX = '''---
Diese Nachricht wurde aus dem Kontaktformular der Website des Aikido Dojo Seishinkan verschickt.
http://www.aikido-dojo-seishinkan.de/
'''

SSL_URLS = [
    r'/log/',
    r'/login/',
    r'/logout/',
    r'/email/',
    r'/graduierungen/',
    r'/mitglieder/',
    r'/mitgliederliste/',
    r'/permissions/',
    r'/verwaltung/',
    r'/rosetta/',
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ugettext = lambda s: s
LANGUAGES = (
    ('de', ugettext(u'Deutsch')),
    ('en', ugettext(u'English')),
    ('ja', ugettext(u'日本語')),
)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

# MIDDLEWARE_CLASSES = (
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.locale.LocaleMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.middleware.doc.XViewMiddleware',
#     'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
#     'seishinkan.utils.ssl.SSLRedirect',
# )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'seishinkan.utils.ssl.SSLRedirect',
 )

ROOT_URLCONF = 'seishinkan.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'seishinkan.website',
    'seishinkan.members',
    'seishinkan.news',
    'seishinkan.links',
    'rosetta',
)

try:
    from mysettings import *
except ImportError:
    pass
