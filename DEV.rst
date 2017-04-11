Dev setup and deployment notes.


Settings
------------

global_finprint relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**.
It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps the 'global_finprint' environment variables to their Django setting:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DJANGO_DATABASE_URL                     DATABASES (default)         postgres:///global_finprint                    n/a

DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
DJANGO_MEDIA_ROOT                       MEDIA_ROOT                  APPS_DIR('media')                              APPS_DIR('media')

DJANGO_SERVER_ENV                       DJANGO_SERVER_ENV           local                                          prod
======================================= =========================== ============================================== ======================================================================

The following table lists settings and their defaults for third-party applications:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DJANGO_AWS_ACCESS_KEY_ID                AWS_ACCESS_KEY_ID           n/a                                            raises error
DJANGO_AWS_SECRET_ACCESS_KEY            AWS_SECRET_ACCESS_KEY       n/a                                            raises error
DJANGO_AWS_STORAGE_BUCKET_NAME          AWS_STORAGE_BUCKET_NAME     n/a                                            raises error
======================================= =========================== ============================================== ======================================================================

Getting up and running
----------------------

Basics
^^^^^^

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv
* PostgreSQL
* PostGIS

First make sure to create and activate a Python venv, then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements/local.txt

Create a local PostgreSQL database::

    $ createdb global_finprint

Run ``migrate`` on your new database::

    $ python manage.py migrate



You can now run the ``runserver_plus`` command::

    $ python manage.py runserver_plus

Open up your browser to http://127.0.0.1:8000/ to see the site running locally.

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you'd like to take advantage of live reloading and Sass / Compass CSS compilation you can do so with a little bit of prep work.

Make sure that nodejs_ is installed. Then in the project root run::

    $ npm install

.. _nodejs: http://nodejs.org/download/

If you don't already have it, install `compass` (doesn't hurt if you run this command twice)::

    gem install compass

Now you just need::

    $ grunt serve

The base app will now run as it would with the usual ``manage.py runserver`` but with live reloading and Sass compilation enabled.

To get live reloading to work you'll probably need to install an `appropriate browser extension`_

.. _appropriate browser extension: http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions-


Celery
^^^^^^
This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd global_finprint
    celery -A global_finprint worker -l info

Please note: For Celerys import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.



It's time to write the code!!!


Deployment
------------

It is possible to deploy to Heroku or to your own server by using Dokku, an open source Heroku clone.

Heroku
^^^^^^

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python

    heroku addons:create heroku-postgresql:hobby-dev
    heroku pg:backups schedule --at '02:00 America/Los_Angeles' DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:create heroku-redis:hobby-dev
    heroku addons:create mailgun

    heroku config:set DJANGO_SECRET_KEY=`openssl rand -base64 32`
    heroku config:set DJANGO_SETTINGS_MODULE='config.settings.production'

    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE

    heroku config:set DJANGO_MAILGUN_SERVER_NAME=YOUR_MALGUN_SERVER
    heroku config:set DJANGO_MAILGUN_API_KEY=YOUR_MAILGUN_API_KEY

    heroku config:set PYTHONHASHSEED=random

    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open

Dokku
^^^^^

You need to make sure you have a server running Dokku with at least 1GB of RAM. Backing services are
added just like in Heroku however you must ensure you have the relevant Dokku plugins installed.

.. code-block:: bash

    cd /var/lib/dokku/plugins
    git clone https://github.com/rlaneve/dokku-link.git link
    git clone https://github.com/luxifer/dokku-redis-plugin redis
    git clone https://github.com/jezdez/dokku-postgres-plugin postgres
    dokku plugins-install

You can specify the buildpack you wish to use by creating a file name .env containing the following.

.. code-block:: bash

    export BUILDPACK_URL=<repository>

You can then deploy by running the following commands.

..  code-block:: bash

    git remote add dokku dokku@yourservername.com:global_finprint
    git push dokku master
    ssh -t dokku@yourservername.com dokku redis:create global_finprint-redis
    ssh -t dokku@yourservername.com dokku redis:link global_finprint-redis global_finprint
    ssh -t dokku@yourservername.com dokku postgres:create global_finprint-postgres
    ssh -t dokku@yourservername.com dokku postgres:link global_finprint-postgres global_finprint
    ssh -t dokku@yourservername.com dokku config:set global_finprint DJANGO_SECRET_KEY=RANDOM_SECRET_KEY_HERE
    ssh -t dokku@yourservername.com dokku config:set global_finprint DJANGO_SETTINGS_MODULE='config.settings.production'
    ssh -t dokku@yourservername.com dokku config:set global_finprint DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    ssh -t dokku@yourservername.com dokku config:set global_finprint DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    ssh -t dokku@yourservername.com dokku config:set global_finprint DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE
    ssh -t dokku@yourservername.com dokku config:set global_finprint DJANGO_MAILGUN_API_KEY=YOUR_MAILGUN_API_KEY
    ssh -t dokku@yourservername.com dokku config:set global_finprint DJANGO_MAILGUN_SERVER_NAME=YOUR_MAILGUN_SERVER
    ssh -t dokku@yourservername.com dokku run global_finprint python manage.py migrate
    ssh -t dokku@yourservername.com dokku run global_finprint python manage.py createsuperuser

When deploying via Dokku make sure you backup your database in some fashion as it is NOT done automatically.
