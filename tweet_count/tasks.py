from birdy.twitter import StreamClient
from django.conf import settings
from redis import Redis

from tweet_count.celery import celery


@celery.task
def collect(track='charity'):
    client = StreamClient(
        settings.TWITTER['CONSUMER_KEY'],
        settings.TWITTER['CONSUMER_SECRET'],
        settings.TWITTER['ACCESS_TOKEN'],
        settings.TWITTER['ACCESS_SECRET']
    )

    response = client.stream.statuses.filter.post(track=track)
    for data in response.stream():
        # the streaming api seems to be a bit
        # tempermental at times with regards to
        # consistently returning all keys
        if 'hashtags' in data.get('entities', {}):
            process.delay(data)


@celery.task
def process(tweet):
    """
    Responsible for picking out
    hashtags from JSON and updating
    redis
    """
    redis = Redis.from_url(settings.REDIS_GENERAL)
    for tag in tweet['entities']['hashtags']:
        hashtag = tag['text'].encode('utf8').lower()
        result = redis.zincrby('hashtags', hashtag, 1)
        print 'Incremented %s: %s' % (hashtag, result)
