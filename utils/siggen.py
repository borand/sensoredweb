"""siggen.py - signal generator used to submit test data to sensordata app 

Usage:  
  siggen.py [--ip=IP_ADDRESS | --port=REMOTE_PORT | --num=NUM_OF_SAMPLES | --dt=PERIOD] 
  siggen.py (-h | --help)

Options:
  -h, --help  
  --ip=IP_ADDRESS      [default: 127.0.0.1]
  --port=REMOTE_PORT   [default: 8000]
  --num=NUM_OF_SAMPLES [default: 60]
  --dt=PERIOD          [default: 1]
"""

import math
import datetime
import time
from docopt import docopt
from math import sin, cos, pi
from requests import get

def siggen(num_of_samples=60, dt=1, ip='127.0.0.1', port=8000):
    """
    """
    serial_number = '0'
    to = datetime.datetime.now()
    T = 0.1
    for i in range(num_of_samples):
        tn = datetime.datetime.now()
        t  = float((tn-to).seconds)
        ys  = 2.0*sin(T * t)
        yc  = 2.0*cos(T * t)
        #print t, ys, yc
        time.sleep(dt)        
        #get('http://10.128.124.166/sensordata/api/submit/datavalue/%s/sn/%s/val/%.3f' % (tn.strftime('%Y-%m-%d-%H:%M:%S'), 'sin', y))
        outs = get('http://%s:%d/sensordata/api/submit/datavalue/%s/sn/%s/val/%.3f' \
                    % (ip, port, tn.strftime('%Y-%m-%d-%H:%M:%S'), serial_number, ys))
        #outc = get('http://192.168.1.111:8000/sensordata/api/submit/datavalue/%s/sn/%s/val/%.3f' % (tn.strftime('%Y-%m-%d-%H:%M:%S'), '1', yc))
        print outs.content

def populate(num_of_samples=3600,dt=1, ip='127.0.0.1', port=8000,freq=0.1,serial_number='0'):
    
    to = datetime.datetime(2012,02,01)        
    for i in range(num_of_samples):
        delta_time = datetime.timedelta(seconds=i*dt)
        tn = to + delta_time
        t  = float((tn-to).seconds)
        ys  = 2.0*sin(freq * t)        
        outs = get('http://%s:%d/sensordata/api/submit/datavalue/%s/sn/%s/val/%.3f' % (ip, port, tn.strftime('%Y-%m-%d-%H:%M:%S'), serial_number, ys))
        print i, outs.content
         
    
if __name__ == '__main__':
    arguments = docopt(__doc__)