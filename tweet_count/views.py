from django.conf import settings
from django.http import HttpResponse

from redis import Redis

from .util import json_response

redis = Redis.from_url(settings.REDIS_GENERAL)


def index(request):
    return HttpResponse('placeholder')


@json_response
def count(request):
    redis_set = redis.zrevrangebyscore(
        'hashtags',
        min=1,
        max='+inf',
        withscores=True,
        score_cast_func=int,
    )

    hashtags = [{
        'hashtag': tag[0],
        'count': tag[1],
    } for tag in redis_set]
    return hashtags
