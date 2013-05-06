from __future__ import absolute_import

import os
from celery import Celery
from celery_tocloud.app import celeryconfig

celery = Celery()

celery.config_from_object(celeryconfig)

celery.conf.update(
    CELERY_IMPORTS = (
    	'celery_tocloud.app.tasks',
    ),
)

if __name__ == '__main__':
    celery.start()