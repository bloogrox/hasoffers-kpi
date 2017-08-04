from .base import *


SECRET_KEY = '*!678w4fc%'

DEBUG = True

ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
    'localhost'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}


CELERY_BROKER_URL = "amqp://guest:guest@rabbitmq:5672"  # os.environ['RABBITMQ_BIGWIG_URL']


HASOFFERS_NETWORK_ID = ''
HASOFFERS_NETWORK_TOKEN = ''

MANAGER_EMAIL = ''

NETWORK_EMAIL = ''

CLICK_COST = 600 / 1000000

SENDGRID_API_KEY = ''


SITE_URL = 'http://127.0.0.1:8000'
