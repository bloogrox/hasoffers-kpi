from .base import os
# import os
import dj_database_url


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# TIME_ZONE = 'Asia/Jerusalem'
TIME_ZONE = 'America/New_York'


DATABASE_URL = os.environ['DATABASE_URL']

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, engine='django.db.backends.postgresql_psycopg2')
}


CELERY_BROKER_URL = os.environ['RABBITMQ_BIGWIG_URL']


HASOFFERS_NETWORK_ID = os.environ['HASOFFERS_NETWORK_ID']
HASOFFERS_NETWORK_TOKEN = os.environ['HASOFFERS_NETWORK_TOKEN']

MANAGER_EMAIL = os.environ['MANAGER_EMAIL']

NETWORK_EMAIL = os.environ['NETWORK_EMAIL']

SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']

CLICK_COST = int(os.environ['HASOFFERS_CLICKS_COST']) / 1000000

SITE_URL = os.environ['SITE_URL']


PROXIES = {
    'http': os.environ['PROXIMO_URL'],
    'https': os.environ['PROXIMO_URL']
}
