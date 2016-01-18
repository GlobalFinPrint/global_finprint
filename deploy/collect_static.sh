#!/bin/bash
source ./set_env.sh

cd $DJANGO_DIR
./manage.py collectstatic -v0 --noinput
