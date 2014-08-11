
"""clonemodels.py - copies models from one db to another

Usage:
  clonemodels.py [tofile]
  clonemodels.py run [--ip=IP_ADDRESS] [tofile]
  clonemodels.py (-h | --help)

Options:
  -h, --help
  --ip=IP_ADDRESS      [default: 127.0.0.1]
"""

__author__ = 'andrzej'


from requests import get, post
import simplejson as sj
from docopt import docopt



old_host      = 'http://sensoredweb.herokuapp.com/sensordata/api'
old_host_auth = ('pandas','misuszatek')

new_host      = '192.168.1.10';
new_host      = '0.0.0.0';
new_host_auth = ('andrzej','admin')
root_url      =  'http://{0}:8000/sensordata/api'.format(new_host)
headers       = {'content-type': 'application/json'}
print root_url



def get_json(host, host_auth, model):
    out = get('{0}/{1}/.json'.format(old_host, model), auth=old_host_auth)
    if out.ok:
        return out.json()
    else:
        return []

def set_model_data(root_url, host_auth, model, data, headers={'content-type': 'application/json'}):
    if len(data) > 0:
        for i in data:
            #print unit
            payload = sj.dumps(i)
            print payload
            p = post('{0}/{1}/'.format(root_url,model), data=payload, auth=host_auth, headers=headers)
            print p.ok
    else:
        print('Data appears to be empty')


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print arguments
    go     = arguments.get('run',False)
    tofile = arguments.get('tofile',False)

    model_list = ['units', 'man', 'physicalsignal', 'location', 'device', 'gateway', 'deviceinstance']

    if tofile:
        fid=open('./models.json', 'w+')
    for model in model_list:
        data = get_json(old_host, old_host_auth, model)
        print "Model '{0}' : {1}".format(model,len(data))
        if tofile:
            file_line = '{{"{0}":{1}\r\n}}'.format(model,str(data))
            fid.write(file_line)
        if go:
            set_model_data(root_url, new_host_auth, model, data)

    if tofile:
        fid.close()

