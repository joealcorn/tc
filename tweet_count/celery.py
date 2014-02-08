from __future__ import absolute_import
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tweet_count.settings')

celery = Celery('tweet_count')
celery.config_from_object('django.conf:settings')
