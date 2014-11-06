from __future__ import absolute_import

from celery import shared_task, task

import redis
import time
from anyjson import serialize

from ablib.daq.datastore import submit

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def ON(**kwargs):
    r = redis.Redis()
    r.publish('192.168.1.200:-cmd','on')

@shared_task
def OFF(**kwargs):
    r = redis.Redis()
    r.publish('192.168.1.200:-cmd','off')

@shared_task
def flash(**kwargs):
    r = redis.Redis()
    r.publish('192.168.1.200:-cmd','on')
    time.sleep(2)   
    r.publish('192.168.1.200:-cmd','off')

@shared_task
def send_insteon_cmd(*arg, **kwargs):
    r = redis.Redis()
    address = arg[0]
    cmd     = arg[1]
    val     = arg[2]
    insteon_msg = serialize([address, cmd, val])
    r.publish('InsteonPLM',insteon_msg)


@task()
def submit_data(*arg):
    print arg[0]
    submit(arg[0])
