Dev setup notes.


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



Basics
^^^^^^

The steps below will get you up and running with a local development environment. We assume you have the following installed::

* pip
* virtualenv
* PostgreSQL
* PostGIS

First make sure to create and activate a Python venv, e.g.::

    $ python3 -m venv /path/to/new/virtual/environment
    $ source /path/to/new/virtual/environment/bin/activate

Then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements/local.txt

Create a local PostgreSQL database::

    $ createdb global_finprint

Run ``migrate`` on your new database::

    $ python manage.py migrate

Apply the fixtures to add some dev data::

    $ loaddata global_finprint/core/fixtures/core_groups

(see /global_finprint/deploy/loaddata.txt and /global_finprint/deploy/loaddata_test.txt for full lists of fixtures)

Copy /global_finprint/global_finprint/static/version.example.txt to /global_finprint/global_finprint/static/version.txt::

    $ cp /global_finprint/global_finprint/static/version.example.txt /global_finprint/global_finprint/static/version.txt

You can now run the ``runserver_plus`` command::

    $ python manage.py runserver_plus

Open up your browser to http://127.0.0.1:8000/ to see the site running locally.

To create an **superuser account**, use this command::

    $ python manage.py createsuperuser
