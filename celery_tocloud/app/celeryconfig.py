"""
Configuration for the Celery application.

Should use Redis DB's 7-9
"""

from django.conf import settings
from kombu import Exchange, Queue

DEBUG = True

## Dropbox
APP_KEY = '3wt9hriil3ozkwb'
APP_SECRET = 'yqjvj22cenl85bv'
ACCESS_TYPE = 'app_folder'
CHUNK_SIZE = 4194304

## Celery
CELERY_RESULT_BACKEND = 'redis://localhost/7'

CELERY_DEFAULT_QUEUE = 'downloads'

CELERY_TIMEZONE = 'America/Toronto'

CELERY_IGNORE_RESULT 	= False

CELERY_DEFAULT_EXCHANGE = 'tocloud'

CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'

CELERY_DEFAULT_ROUTING_KEY = 'downloads'

BROKER_URL = 'amqp://localhost'

CELERY_IMPORTS = ('',)

CELERY_TRACK_STARTED = True

## Celery Queues
CELERY_QUEUES = (
	Queue('downloads', routing_key='downloads'),
)

## Environment
if DEBUG is True:
	# Do some different stuff for DEBUG
	pass