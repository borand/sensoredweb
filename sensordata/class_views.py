# Create your views here.
from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.views.generic import ListView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from sensordata.models import DeviceInstance, DataValue, TimeStamp
import simplejson


#from django.template import RequestContext

import datetime
import time
from data_utils import data_value_submission

from django.utils.log import getLogger
logger = getLogger("app")

class ApiDeviceInstanceView(ListView):    
    model = DeviceInstance
    

class ApiDataValueView(TodayArchiveView):
    model = TimeStamp
    queryset = TimeStamp.objects.all()
    date_field = "measurement_timestamp"
    make_object_list = True
    allow_future = True
    
    