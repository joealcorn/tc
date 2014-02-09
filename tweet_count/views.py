from django.conf import settings
from django.shortcuts import render

from redis import Redis

from tweet_count.util import json_response
from tweet_count.tasks import collect

redis = Redis.from_url(settings.REDIS_GENERAL)


def index(request):
    return render(request, 'index.html')


@json_response
def control(request):
    action = request.GET.get('action', 'status')

    if action == 'start':
        collect.delay()
    
    elif action == 'stop':
        redis.publish('collect', 'abort')

    return {'status': redis.get('collect_status')}


@json_response
def count(request):
    redis_set = redis.zrevrangebyscore(
        'hashtags',
        min=1,
        max='+inf',
        start=0,
        num=50,
        withscores=True,
        score_cast_func=int,
    )

    hashtags = [{
        'hashtag': tag[0],
        'count': tag[1],
    } for tag in redis_set]
    return hashtags
