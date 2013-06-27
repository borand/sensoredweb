from django.conf.urls import patterns, url
from sensordata.class_views import ApiDeviceInstanceView, ApiDataValueView, ApiDataValueView
from . import views

urlpatterns = patterns('',    
    url(r'^$',views.HomePageView.as_view(), name='home'),
    url(r'^ping$','sensordata.views.ping', name='ping'),
    
    url(r"^devices/", views.DeviceInstanceView.as_view(), name="device_instance_list"),    

    url(r"^test/(?P<serial_number>[a-zA-Z0-9-_]+)", views.ApiDataValueView.as_view(), name="api_get_datavalue"),    
    
    ## SUBMIT DATA
    url(r'^api/submit/datavalue/(?P<datestamp>now)/sn/(?P<sn>.*)/val/(?P<val>.*)$','sensordata.views.api_submit_datavalue', name='apt_datavalue'),
    url(r'^api/submit/datavalue/(?P<datestamp>\d{4}\-\d{1,2}\-\d{1,2}-\d{1,2}:\d{1,2}:\d{1,2}\.*\d{0,6})/sn/(?P<sn>.*)/val/(?P<val>.*)$','sensordata.views.api_submit_datavalue', name='apt_datavalue'),
    
    
    url(r'^api/datavalue/(?P<device>[a-zA-Z0-9-_]+)/(?P<today>)today','sensordata.views.api_get_datavalue', name='data_value_api'),    
    url(r'^api/datavalue/(?P<device>[a-zA-Z0-9-_]+)/from/(?P<from>\d{4}\-\d{1,2}\-\d{1,2})/to/(?P<to>\d{4}\-\d{1,2}\-\d{1,2})','sensordata.views.api_get_datavalue', name='data_value_api'),
    url(r'^api/datavalue/(?P<device>[a-zA-Z0-9-_]+)','sensordata.views.api_get_datavalue', name='data_value_api'),    
    url(r'^api/datavalue/(?P<device>[a-zA-Z0-9-_]+).json?callback=?$','sensordata.views.api_get_datavalue', name='data_value_api'),
)


#<ul>
#    {% for dev in deviceinstance_list %}
#    <li><a>{{dev.device}}, {{dev.device.model_number}},{{dev.serial_number}} </a></li>
#    {% empty %}
#    <li>Sorry, no devices added. Check back soon!</li>
#    {% endfor %}
#</ul>