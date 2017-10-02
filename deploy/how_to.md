**Deployment**

Files in this directory:
1) nginx.conf (configuration for Nginx - not using sites-enabled, just overrides default) 
2) gunicorn.conf.py (Gunicorn configuration)
3) global_finprint.conf (for Upstart)
4) set_env.sh.template (template for environment variables needed by Django, including AWS and db settings)
5) fabfile.py.template (fabfile that needs host and pem file values added)
6) collect_static.sh (Django manage.py script for collectstatic.  requires set_env.sh)
7) run_gunicorn.sh (starts Gunicorn.  requires set_env.sh)

To build fresh deployment:
1) install fabric if you haven't already
2) spin up a clean instance of Ubuntu 14.04
3) create a database instance, empty database and deploy migrations
4) copy set_env.sh.template to set_env.sh and fill in the necessary values
5) copy fabfile.py.template to fabfile.py and fill in the necessary values
6) fab create (will ask for GitHub username and password during process)
7) enjoy 

To update with commited changes:
1) fab deploy (will ask for GitHub username and password during process)
