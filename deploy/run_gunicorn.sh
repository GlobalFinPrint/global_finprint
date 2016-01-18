#!/bin/bash

cd $DJANGO_DIR
source ./set_env.sh
exec $VIRTUAL_ENV/bin/gunicorn -c $DJANGO_DIR/config/gunicorn.conf.py config.wsgi
