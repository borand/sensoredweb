"""rtweb.py -

Main webserver for rtweb

Usage:
  rtweb.py [--port=PORT] [--host=HOST]

Options:
  --port=PORT  [default: 8888]

"""

from __future__ import print_function
import uuid
import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.gen
import logging
import tornadoredis
import os
import logbook

from docopt import docopt
#from ablib.util.common import get_host_ip

from redis import Redis

#define("port", default=8888, help="run on the given port", type=int)

##########################################################################################
#
#
def get_host_ip():
    return '127.0.0.1'

log = logbook.Logger('rtweb.py')
redis_host_ip = get_host_ip()
host_ip       = get_host_ip()
redis_pubsub_channel = ('rtweb', 'error')

#c = tornadoredis.Client(host=redis_host_ip)
#c.connect()
R = Redis()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        interfaces = list(R.smembers('ComPort'))
        dynamic_content = { "title" : "RT WEB", "host_ip" : host_ip, "page_title" : 'Test', "interfaces" : interfaces}
        self.render("rtweb.html", title="RT WEB", host_ip=host_ip, page_title='Test', interfaces=interfaces)
        #self.render("rtweb.html", dynamic_content)

class ConsoleHandler(tornado.web.RequestHandler):
    def get(self):
        interfaces = list(R.smembers('ComPort'))      
        self.render("console.html", title="RTConsole", host_ip=host_ip, page_title='Test', interfaces=interfaces)

class CmdHandler(tornado.web.RequestHandler):
    def get(self):
        cmd  = self.get_argument("cmd", None)
        chan = self.get_argument("chan", None)
        #msg  = simplejson.dumps({'cmd' : cmd, 'chan' : chan, 'res' : 'OK'})
        #self.write('cmd= %s  para= %s' % (cmd, para))
        #print('CmdHandler(%s)' % cmd)
        #self.write(msg)
        R.publish(chan + '-cmd',cmd)

class NewMessageHandler(tornado.web.RequestHandler):
    def post(self):
        message = self.get_argument('message')
        R.publish(redis_pubsub_channel, message)
        self.set_header('Content-Type', 'text/plain')
        self.write('sent: %s' % (message,))

class MessageHandler(tornado.websocket.WebSocketHandler):

    channel = 'comport'

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True


    def open(self, chan):
        self.sub_channel = chan
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.client = tornadoredis.Client(redis_host_ip)
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, self.sub_channel)
        self.client.listen(self.on_message)

    def on_message(self, msg):        
        #log.debug(type(msg))
        if isinstance(msg,unicode):
            log.debug(msg)
        else:
            if msg.kind == 'message':
                #log.debug(str(simplejson.loads(msg.body)))
                self.write_message(str(msg.body))
            if msg.kind == 'disconnect':
                # Do not try to reconnect, just send a message back
                # to the client and close the client connection
                self.write_message('The connection terminated '
                                   'due to a Redis server error.')
                self.close()

    def on_close(self):
        if self.client.subscribed:
            self.client.unsubscribe(redis_pubsub_channel)
            self.client.disconnect()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r'/', MainHandler),
                (r'/console', ConsoleHandler),
                (r'/cmd/', CmdHandler),
                (r'/msg', NewMessageHandler),
                (r'/websocket/(?P<chan>.*)', MessageHandler),
                ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    print("=== RTWEB ===")
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)
    port = int(arguments['--port'])
    app = Application()
    app.listen(port)
    print('RTWEB is running at %s:%d\nQuit the demo with CONTROL-C' % (get_host_ip(), port))
    tornado.ioloop.IOLoop.instance().start()