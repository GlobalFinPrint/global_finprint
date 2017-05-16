Dev setup notes.


Settings
------------

For configuration purposes, the following table maps the 'global_finprint' environment variables to their Django setting:
======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DJANGO_DATABASE_URL                     DATABASES (default)         postgres:///global_finprint                    n/a

DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
DJANGO_MEDIA_ROOT                       MEDIA_ROOT                  APPS_DIR('media')                              APPS_DIR('media')

DJANGO_SERVER_ENV                       DJANGO_SERVER_ENV           local                                          prod
DJANGO_ALLOWED_HOSTS                    ALLOWED_HOSTS               none (you probably want to set to '127.0.0.1') .globalfinprint.org
                                                                    note that this is a list.
======================================= =========================== ============================================== ======================================================================

The following table lists settings and their defaults for third-party applications:

======================================= =========================== ============================================== ======================================================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ======================================================================
DJANGO_AWS_ACCESS_KEY_ID                AWS_ACCESS_KEY_ID           n/a                                            raises error
DJANGO_AWS_SECRET_ACCESS_KEY            AWS_SECRET_ACCESS_KEY       n/a                                            raises error
DJANGO_AWS_STORAGE_BUCKET_NAME          AWS_STORAGE_BUCKET_NAME     n/a                                            raises error
======================================= =========================== ============================================== ======================================================================
See https://django-environ.readthedocs.io/en/latest/ for more info on setting env variables.


Basics
^^^^^^

The steps below will get you up and running with a local development environment. We assume you have the following installed::

* pip
* virtualenv
* PostgreSQL
* PostGIS
* Bower

First make sure to create and activate a Python venv, e.g.::

    $ python3 -m venv /path/to/new/virtual/environment
    $ source /path/to/new/virtual/environment/bin/activate

Then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements/local.txt

Create a local PostgreSQL database::

    $ createdb global_finprint

Either
  1)
    Run ``migrate`` on your new database and apply the fixtures to add some dev data
    (see /global_finprint/deploy/loaddata.txt and /global_finprint/deploy/loaddata_test.txt for full lists of fixtures)::

    $ python manage.py migrate
    $ loaddata global_finprint/core/fixtures/core_groups

  or 2)
    Add the postgis extensions to the database, restore a dump and catch up with any subsequent migrations::

    $ psql -d global_finprint -c 'create extension postgis;'
    $ pg_restore -d global_finprint /path/to/database.dump
    $ python manage.py migrate

Copy /global_finprint/global_finprint/static/version.example.txt to /global_finprint/global_finprint/static/version.txt::

    $ cp /global_finprint/global_finprint/static/version.example.txt /global_finprint/global_finprint/static/version.txt

Navigate to the project directory and use Bower to install web componenets::

    $ bower install

You can now run the ``runserver_plus`` command::

    $ python manage.py runserver_plus

Open up your browser to http://127.0.0.1:8000/ to see the site running locally.

To create an **superuser account**, use this command::

    $ python manage.py createsuperuser
