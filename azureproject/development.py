import os
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = "this secret"

# Don't use Whitenoise to avoid having to run collectstatic first.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

ALLOWED_HOSTS = ['*']

# Configure connection setting for local PostgreSQL instance.
# Set these environment variables in the .env file for this project.  

# Local to instance settings.
DBHOST="host.docker.internal"
DBNAME="bot_pedido"
DBUSER="postgres"
DBPASS="postgres"

# Configure database connection for remote PostgreSQL instance.
if 'USE_REMOTE_POSTGRESQL' in os.environ:
    DBNAME=os.environ['AZURE_POSTGRESQL_DATABASE']
    DBHOST=os.environ['AZURE_POSTGRESQL_HOST']
    DBUSER=os.environ['AZURE_POSTGRESQL_USERNAME']
    DBPASS=os.environ['AZURE_POSTGRESQL_PASSWORD']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DBNAME,
        'HOST': DBHOST,
        'USER': DBUSER,
        'PASSWORD': DBPASS,
    }
}
