#!/bin/bash

# Replace these three settings.
PROJDIR="/home/marcus/seishinkan/seishinkan"
PIDFILE="$PROJDIR/seishinkan.pid"
SOCKET="$PROJDIR/seishinkan.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE
