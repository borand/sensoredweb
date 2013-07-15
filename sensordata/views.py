# Create your views here.
from django.contrib.auth import authenticate, login
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from sensordata import models
# from utils.management import get_host_ip, restart_fcgi, is_fcgi_running
import simplejson

#from django.template import RequestContext

import datetime
import time
from data_utils import data_value_submission

from django.utils.log import getLogger
logger = getLogger("app")

#########################################################################
#
# Group of Home views
#
def ping(request):
    msg = "pong %s" % (datetime.datetime.now())
    logger.info(msg)    
    return HttpResponse(msg)

class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        
        msg = "you are home @ %s" % (datetime.datetime.now())        
        context = super(HomePageView, self).get_context_data(**kwargs)        
        # context['device_instance'] = models.DeviceInstance.objects..filter(private=False).order_by('device')
        context['msg'] = msg
        logger.info(msg)
        return context

########################################################################
#
# Basic object display classes
#
class DeviceInstanceView(ListView):
    
    def get_queryset(self):
        if self.request.user.is_authenticated():
            return models.DeviceInstance.objects.filter(user=self.request.user).order_by('device')
        else:
            return models.DeviceInstance.objects.filter(private=False).order_by('device')

class DataValueView(ListView):
    model = models.DataValue

#######################################################################################
#
# API Classes
#
class ApiDataValueView(View):

    def get(self, request, *args, **kwargs):        
        serial_number = kwargs['serial_number']
        print "Serial Number =" + '"'+ serial_number + '"'
        items  = models.DataValue.objects.filter(device_instance__serial_number=serial_number).order_by('data_timestamp__measurement_timestamp')                
        return HttpResponse(str(items[0]))

#######################################################################################
#
# API
#
def api_control(request):
    logger.debug("api_control()")
    cmd = request.GET.get('cmd')
    val = request.GET.get('val')
        
    logger.debug("api_control(cmd = %s, val = %s)" % (cmd, str(val)))
    if "ping" in cmd:
        logger.debug("\trespondng to ping")
        response = '"pong"'
    elif "data_entry" in cmd:
        logger.debug("\trespondng to data_entry : val= %s" % val)
        submitted_data = simplejson.loads(val)         
        response  = data_value_submission('now', submitted_data[0], submitted_data[1],request.META.get('REMOTE_ADDR'))
    else:
        response = '"none"' 
        
        
    #response = '"main_io cmd=%s, val=%s time=%s"' %  (cmd,val,datetime.datetime.now())    
    logger.debug('response = %s' % response)    
    return HttpResponse(response, content_type="text/json")

#######################################################################################
# API
#
def api_get_device_instance(request, **kwargs):
    print kwargs
    items = models.DeviceInstance.objects.all() #filter(keyword=kwargs['keyword'])
    items = serializers.serialize('json', items, indent=4)
    return HttpResponse(items, mimetype='application/json')

def api_submit_datavalue(request, datestamp, sn, val):
    msg = "[SUBMITTED] datestamp: %s, sn: %s, val: %s" % (datestamp, sn, val)
    logger.info(msg)
    results = data_value_submission(datestamp, sn, val, request.META.get('REMOTE_ADDR'))
    return HttpResponse(msg + results)

def api_get_datavalue(request, **kwargs):
    to = time.time()
    callback = request.GET.get('callback', '')
    logger.debug('callback: ' + callback)
    logger.debug("Filtering: %s, ajax request=%s" % (str(kwargs),str(request.is_ajax())))    

    items  = models.DataValue.objects.filter(device_instance__serial_number=kwargs['device']).order_by('data_timestamp__measurement_timestamp')

    logger.debug("Query time             = %.3f" % (time.time() - to))
        
    if kwargs.has_key('today'):
        logger.debug("Filtering: todays data")        
        items = items.filter(data_timestamp__measurement_timestamp__gte=datetime.date.today())
            
    if kwargs.has_key('from') and kwargs.has_key('to'):
        start_date = datetime.datetime.strptime(kwargs['from'].split('.')[0],"%Y-%m-%d")
        end_date   = datetime.datetime.strptime(kwargs['to'].split('.')[0],"%Y-%m-%d")
        items = items.filter(data_timestamp__measurement_timestamp__range=(start_date, end_date))

    logger.debug("Found %d items matching criteria " % items.count())
    values_list = items.values_list('data_timestamp__measurement_timestamp','value')    
    v = items.values_list('value',flat=True)
    t = items.values_list('data_timestamp__measurement_timestamp',flat=True)
    logger.debug("Making the list        = %.3f" % (time.time() - to))
    
    logger.debug("Preparing array for json transmision")
    data = []
    for data_pt in values_list:        
        data.append([time.mktime(data_pt[0].timetuple())*1000,data_pt[1]])


    logger.debug("Making value pair list = %.3f" % (time.time() - to))
    
    #items      = serializers.serialize('json', values)
    data_dict = {'data': data, 'serial_number': kwargs['device']}
    #data_dict = [{'data' : data, 'name' : kwargs['device']}]    
    json_out   = simplejson.dumps(data_dict)    
#    json_out   = simplejson.dumps(data) 
    logger.debug("Converting to json     = %.3f" % (time.time() - to))
    if request.is_ajax():
        mimetype='text/json'
    else:
        mimetype='text/json'        
        mimetype='application/json'
        #mimetype='text/json'

    
#    req = {}
#    req ['title'] = 'This is a constant result.'
#    response = simplejson.dumps(req)
    if 'highcharts' in callback:
        response = callback + '(' + json_out + ');'
    else:
        response = json_out

    if not request.user.is_authenticated():
        response = "not authorized"

    return HttpResponse(response, mimetype=mimetype,content_type='application/json')