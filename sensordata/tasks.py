from __future__ import absolute_import

from celery import shared_task

import redis

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


def send_message(**kwargs):
	pass
