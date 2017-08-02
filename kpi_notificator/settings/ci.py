import os
import dj_database_url
from .base import *  # noqa


SECRET_KEY = '*!678w4fc%'

DEBUG = True

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
    'localhost'
]


DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        engine='django.db.backends.postgresql_psycopg2'
    )
}


CELERY_BROKER_URL = os.environ['AMQP_URI']


HASOFFERS_NETWORK_ID = ''
HASOFFERS_NETWORK_TOKEN = ''

MANAGER_EMAIL = ''

NETWORK_EMAIL = ''

CLICK_COST = 600 / 1000000

SENDGRID_API_KEY = ''


SITE_URL = 'http://127.0.0.1:8000'