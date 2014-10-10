from __future__ import absolute_import

import os
import redis
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensoredweb.settings')

app = Celery('sensoredweb')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('debug_task')

@app.task(bind=True)
def publish(self):
	r = redis.Redis()
	r.publish('celery','I am here')