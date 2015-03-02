import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.append('/home/marcus/env/seishinkan/lib/python2.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'seishinkan.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
