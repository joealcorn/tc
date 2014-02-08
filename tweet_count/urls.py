from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'tweet_count.views.index', name='index'),
    url(r'^api/1/count$', 'tweet_count.views.count', name='count'),
    url(r'^api/1/control$', 'tweet_count.views.control', name='control'),
)
