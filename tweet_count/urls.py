from django.conf.urls import patterns, url
from django_sse.redisqueue import RedisQueueView

urlpatterns = patterns(
    '',
    url(r'^$', 'tweet_count.views.index', name='index'),
    url(r'^api/1/count$', 'tweet_count.views.count', name='count'),
    url(r'^api/1/control$', 'tweet_count.views.control', name='control'),
    url(r'^api/1/stream$', RedisQueueView.as_view(), name="stream"),
)
