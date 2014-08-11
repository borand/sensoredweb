import time
import datetime
import simplejson

# Create your views here.
from django.contrib.auth import authenticate, login
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.log import getLogger

from sensordata import models

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

        msg = "Sensordata app loaded @ %s" % (datetime.datetime.now())
        context = super(HomePageView, self).get_context_data(**kwargs)
        # context['device_instance'] = models.DeviceInstance.objects..filter(private=False).order_by('device')
        context['msg'] = msg
        logger.info(msg)
        return context

class GatewayMonView(TemplateView):

    template_name = "gatewaymon.html"

    def get_context_data(self, **kwargs):

        msg = "GatewayMonView app loaded @ %s" % (datetime.datetime.now())
        context = super(GatewayMonView, self).get_context_data(**kwargs)
        context['msg'] = msg
        logger.info(msg)
        logger.info(kwargs)
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

class GatewayView(ListView):

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return models.DeviceGateway.objects.all()
        else:
            return models.DeviceGateway.objects.all()

class HomeApi(TemplateView):

    template_name = "sensordata/sensordata_api.html"

    def get_context_data(self, **kwargs):
        
        msg = "you are api home @ %s" % (datetime.datetime.now())        
        context = super(HomeApi, self).get_context_data(**kwargs)        
        # context['device_instance'] = models.DeviceInstance.objects..filter(private=False).order_by('device')
        #context['msg'] = msg
        logger.info(msg)
        return context




#######################################################################################
# JUNK YARD
#

 # def api_get_device_instance(request, **kwargs):
 #    print kwargs
 #    items = models.DeviceInstance.objects.all() #filter(keyword=kwargs['keyword'])
 #    items = serializers.serialize('json', items, indent=4)
 #    return HttpResponse(items, mimetype='application/json')

#  def api_get_datavalue(request, **kwargs):
#     to = time.time()
#     callback = request.GET.get('callback', '')
#     logger.debug('callback: ' + callback)
#     logger.debug("Filtering: %s, ajax request=%s" % (str(kwargs),str(request.is_ajax())))    

#     items  = models.DataValue.objects.filter(device_instance__serial_number=kwargs['device']).order_by('data_timestamp__measurement_timestamp')

#     logger.debug("Query time             = %.3f" % (time.time() - to))
        
#     if kwargs.has_key('today'):
#         logger.debug("Filtering: todays data")        
#         items = items.filter(data_timestamp__measurement_timestamp__gte=datetime.date.today())
            
#     if kwargs.has_key('from') and kwargs.has_key('to'):
#         start_date = datetime.datetime.strptime(kwargs['from'].split('.')[0],"%Y-%m-%d")
#         end_date   = datetime.datetime.strptime(kwargs['to'].split('.')[0],"%Y-%m-%d")
#         items = items.filter(data_timestamp__measurement_timestamp__range=(start_date, end_date))

#     logger.debug("Found %d items matching criteria " % items.count())
#     values_list = items.values_list('data_timestamp__measurement_timestamp','value')    
#     v = items.values_list('value',flat=True)
#     t = items.values_list('data_timestamp__measurement_timestamp',flat=True)
#     logger.debug("Making the list        = %.3f" % (time.time() - to))
    
#     logger.debug("Preparing array for json transmision")
#     data = []
#     for data_pt in values_list:        
#         data.append([time.mktime(data_pt[0].timetuple())*1000,data_pt[1]])


#     logger.debug("Making value pair list = %.3f" % (time.time() - to))
    
#     #items      = serializers.serialize('json', values)
#     data_dict = {'data': data, 'serial_number': kwargs['device']}
#     #data_dict = [{'data' : data, 'name' : kwargs['device']}]    
#     json_out   = simplejson.dumps(data_dict)    
# #    json_out   = simplejson.dumps(data) 
#     logger.debug("Converting to json     = %.3f" % (time.time() - to))
#     if request.is_ajax():
#         mimetype='text/json'
#     else:
#         mimetype='text/json'        
#         mimetype='application/json'
#         #mimetype='text/json'
# #    req = {}
# #    req ['title'] = 'This is a constant result.'
# #    response = simplejson.dumps(req)
#     if 'highcharts' in callback:
#         response = callback + '(' + json_out + ');'
#     else:
#         response = json_out

#     if not request.user.is_authenticated():
#         logger.debug("user = %s" % request.user)
#         response = "not authorized"

#     return HttpResponse(response, mimetype=mimetype,content_type='application/json')