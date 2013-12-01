"""Usage:
  submit.py [--redis_host=REDIS_HOST] [--port=REMOTE_PORT] [--dataserver=DATA_SERVER]  
  submit.py -h | --help | --version

Options:
  -h, --help    
  --redis_host=REDIS_HOST   [default: 192.168.1.127]
  --port=REMOTE_PORT        [default: 80]
  --dataserver=DATA_SERVER  [default: sensordata.herokuapp.com]

"""

from docopt import docopt
from requests import get
from redis import Redis


if __name__ == '__main__':    
    arguments = docopt(__doc__)
    print(arguments)
    print arguments['--redis_host']
    # full_url = 'http://%s:%d/sensordata/api/submit/datavalue/%s/sn/%s/val/%.3f' \
    #     % (ip, port, tn.strftime('%Y-%m-%d-%H:%M:%S'), serial_number, ys)
    
    # res = get(full_url)