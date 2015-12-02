from __future__ import absolute_import

from celery import shared_task, task

import redis
import time
from anyjson import serialize

from ablib.daq.datastore import submit

insteon_cmd_chan = 'cmd:insteon'

devices = {
'19.74.73' : 'Serial PLM',
'18.1d.04' : 'dining_room',
'09.8E.94' : 'living_room',
'18.98.AA' : 'livingroom_dimmer',
'16.83.87' : 'livingroom_lamp_sw',
'14.a1.28' : 'outdoor',
'20.1f.11' : 'light',
'1D.AD.86' : 'bedroom',
'1B.7A.50' : 'unused_se',
}


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def send_insteon_cmd(*arg, **kwargs):
	r           = redis.Redis()
	address     = arg[0]
	cmd         = arg[1]
	val         = arg[2]
	insteon_msg = serialize([address, cmd, val])
	r.publish(insteon_cmd_chan,insteon_msg)
	return 'send_insteon_cmd: ' + str(insteon_msg)


@shared_task
def good_morning(*arg, **kwargs):
	r           = redis.Redis()
	msgs = [
		['18.1d.04', 17, 255],
		['09.8E.94', 17, 255],
		['18.98.AA', 17, 255],
		['1D.AD.86', 46, 242],
	]
	for msg in msgs:
		insteon_msg = serialize(msg)
		r.publish(insteon_cmd_chan,insteon_msg)
	return 'good_morning: ' + str(insteon_msg)

@shared_task
def main_floor_on(*arg, **kwargs):
	r           = redis.Redis()
	msgs = [
		['18.1d.04', 17, 255],
		['09.8E.94', 17, 255],
		['18.98.AA', 17, 255],		
	]
	for msg in msgs:
		insteon_msg = serialize(msg)
		r.publish(insteon_cmd_chan,insteon_msg)
	return 'main_floor_on: ' + str(insteon_msg)

@shared_task
def school_time(*arg, **kwargs):
	r           = redis.Redis()
	msgs = [
		['18.1d.04', 19, 0],
		['09.8E.94', 19, 0],
		['18.98.AA', 19, 0],
	]
	for msg in msgs:
		insteon_msg = serialize(msg)
		r.publish(insteon_cmd_chan,insteon_msg)
	return 'school_time: ' + str(insteon_msg)

@shared_task
def christmass_lights_on(*arg, **kwargs):
	r           = redis.Redis()
	msgs = [
		['14.a1.28', 17, 255],
	]
	for msg in msgs:
		insteon_msg = serialize(msg)
		r.publish(insteon_cmd_chan,insteon_msg)
	return 'school_time: ' + str(insteon_msg)

@shared_task
def christmass_lights_off(*arg, **kwargs):
	r           = redis.Redis()
	msgs = [
		['14.a1.28', 19, 0],
	]
	for msg in msgs:
		insteon_msg = serialize(msg)
		r.publish(insteon_cmd_chan,insteon_msg)
	return 'school_time: ' + str(insteon_msg)

@shared_task
def get_status(*arg, **kwargs):
	r           = redis.Redis()
	msg = {"cmd" : "GetStatusOfAllDevices"}
	insteon_msg = serialize(msg)
	r.publish(insteon_cmd_chan, '{\"cmd\": \"GetStatusOfAllDevices\"}')
	return 'get_status: '

@shared_task
def run_cmd(*arg, **kwargs):
	r           = redis.Redis()
	msg  = {"cmd" : kwargs.get("cmd",'GetLightLevel'), "addr" : kwargs.get("addr",'20.1f.11'), "val" : kwargs.get("val",0)}
	insteon_msg = serialize(msg)
	r.publish(insteon_cmd_chan, insteon_msg)
	return 'run_cmd: ' + str(msg)

@shared_task
def publish(*arg, **kwargs):
	r = redis.Redis()
	r.publish(arg[0], arg[1])

