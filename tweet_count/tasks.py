from __future__ import absolute_import

from birdy.twitter import StreamClient
from celery.signals import celeryd_after_setup
from celery.utils.log import get_task_logger
from django.conf import settings
from redis import Redis
import gevent
from tweet_count.celery import celery

redis = Redis.from_url(settings.REDIS_GENERAL)
logger = get_task_logger(__name__)


def listen_for_abort(task):
    pubsub = redis.pubsub()
    pubsub.subscribe('collect')
    for msg in pubsub.listen():
        if msg.get('data') == 'abort':
            task.abort = True


@celery.task(bind=True)
def collect(self, track='charity'):
    """
    Connects to Twitter's streaming api
    and passes tweets off to another task.

    Listens to redis pubsub commands for
    remote control.
    """

    lock = redis.lock('collect_lock')
    if not lock.acquire(blocking=False):
        # Running multiple tasks at once will
        # get us kicked off of Twitter's API
        # https://dev.twitter.com/docs/streaming-apis/streams/public#Connections
        logger.info('Task aready running')
        return

    # Kick off greenlet to listen for
    # pubsub messages
    self.abort = False
    gevent.spawn(listen_for_abort, self)

    redis.set('collect_status', 'Running')
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

        if self.abort:
            # Remove any locks we may have made
            logger.info('Stopping task')
            redis.delete('collect_lock')
            redis.set('collect_status', 'Stopped')
            return


@celery.task
def process(tweet):
    """
    Responsible for picking out
    hashtags from JSON and updating
    redis
    """
    for tag in tweet['entities']['hashtags']:
        hashtag = tag['text'].encode('utf8').lower()
        result = redis.zincrby('hashtags', hashtag, 1)
        logger.info('Incremented #%s: %s' % (hashtag, result))


@celeryd_after_setup.connect
def release_locks(*a, **kw):
    """
    Tasks can't possibly be running, so
    release all locks.
    This prevents CTRL-C from stopping
    tasks from running.
    """
    redis.delete('collect_lock')
    redis.set('collect_status', 'Stopped')
