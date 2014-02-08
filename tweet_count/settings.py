"""
Django settings for tweet_count project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def envbool(key):
    if os.environ.get(key, 'f').lower() in ('t', '1', 'true'):
        return True
    else:
        return False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32).encode('hex'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = envbool('DEBUG')

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = ('django.contrib.staticfiles',)

MIDDLEWARE_CLASSES = []

ROOT_URLCONF = 'tweet_count.urls'

WSGI_APPLICATION = 'tweet_count.wsgi.application'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Redis URLs should be similar to the following:
# redis://username:password@localhost:6379/0
REDIS_CELERY = os.environ.get('REDIS_CELERY', 'redis://localhost:6379/0')
REDIS_GENERAL = os.environ.get('REDIS_GENERAL', 'redis://localhost:6379/1')
