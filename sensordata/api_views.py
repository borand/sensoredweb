# native libraries
import time
import datetime

# django libraries
from django.http import Http404
from django.contrib.auth.models import User
from django.utils.log import getLogger
from django.http import HttpResponse

# rest_framework libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

# sensordata libraries
import serializers
from .serializers import UnitsSerializer2, ManufacturerSerializer, \
                        TimeStampSerializer, DataValueSerializer, DeviceInstanceSerializer,\
                        UserSerializer,TimeStampSerializer,LocationSerializer,\
                        PhysicalSignalSerializer, DeviceSerializer, DeviceGatewaySerializer
from . import models
from .permissions import IsOwnerOrReadOnly
from data_utils import data_value_submission

logger = getLogger("app")
#######################################################################################
# API - usign django-rest-framework
#

# USER
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# UNITS
class UnitstList(generics.ListCreateAPIView):
    queryset = models.Units.objects.all()
    serializer_class = UnitsSerializer2

class UnitsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Units.objects.all()
    serializer_class = UnitsSerializer2

# LOCATIONS
class LocationList(generics.ListCreateAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer

# MANUFACTURER
class ManufacturerList(generics.ListCreateAPIView):
    queryset = models.Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class TimestampList(generics.ListCreateAPIView):
    queryset = models.TimeStamp.objects.all()
    serializer_class = TimeStampSerializer
class TimestampDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TimeStamp.objects.all()
    serializer_class = TimeStampSerializer

class PhysicalSignalList(generics.ListCreateAPIView):
    queryset = models.PhysicalSignal.objects.all()
    serializer_class = PhysicalSignalSerializer
class PhysicalSignalDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.PhysicalSignal.objects.all()
    serializer_class = PhysicalSignalSerializer

class DeviceList(generics.ListCreateAPIView):
    queryset = models.Device.objects.all()
    serializer_class = DeviceSerializer
class DeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceGatewayList(generics.ListCreateAPIView):
    queryset = models.DeviceGateway.objects.all()
    serializer_class = DeviceGatewaySerializer
class DeviceGatewayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DeviceGateway.objects.all()
    serializer_class = DeviceGatewaySerializer

class DeviceInstanceList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    queryset = models.DeviceInstance.objects.all()
    serializer_class = DeviceInstanceSerializer
    def pre_save(self, obj):
        obj.user = self.request.user

class DeviceInstanceDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    queryset = models.DeviceInstance.objects.all()
    serializer_class = DeviceInstanceSerializer

    # def pre_save(self, obj):
    #     obj.user = self.request.user

class DataValueList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    queryset = models.DataValue.objects.all()    
    serializer_class = DataValueSerializer

class DataValueDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    queryset = models.DataValue.objects.all()    
    serializer_class = DataValueSerializer
    # filter_fields = ('device_instance__serial_number')

class DataValueForDevDetail(generics.ListAPIView):      
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    serializer_class   = serializers.DataValuePairSerializer2

    def get_queryset(self):

        logger.debug('get_queryset(kwargs= %s)' % str(self.kwargs))
        to = time.time()
        serial_number = self.kwargs['serial_number']
        queryset = models.DataValue.objects.filter(device_instance__serial_number=serial_number).order_by('data_timestamp__measurement_timestamp')
        logger.debug("Query time             = %.3f" % (time.time() - to))        
        
        if self.kwargs.has_key('today'):
            logger.debug("Filtering: todays data")        
            queryset = queryset.filter(data_timestamp__measurement_timestamp__gte=datetime.date.today())

        if self.kwargs.has_key('from') and self.kwargs.has_key('to'):
            logger.debug("Filtering: from %s to %s" % (self.kwargs.has_key('from'), self.kwargs.has_key('to')))
            start_date = datetime.datetime.strptime(self.kwargs['from'].split('.')[0],"%Y-%m-%d")
            end_date   = datetime.datetime.strptime(self.kwargs['to'].split('.')[0],"%Y-%m-%d")
            queryset = queryset.filter(data_timestamp__measurement_timestamp__range=(start_date, end_date))

        return queryset


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

def api_submit_datavalue(request, datestamp, sn, val):
    msg = "[SUBMITTED] datestamp: %s, sn: %s, val: %s" % (datestamp, sn, val)
    logger.info(msg)
    try:
        results = data_value_submission(datestamp, sn, val, request.META.get('REMOTE_ADDR'))        
    except Exception as E:                
        results = ' Exception: ' + E.message
    return HttpResponse(msg + results)

#######################################################################################
# API - usign django-rest-framework - PART 1
#
# # Only needed for the first part of the tutorial
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders it's content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

#######################################################################################
# API - usign django-rest-framework - PART 2
#
# @api_view(['GET', 'POST'])
# #@csrf_exempt
# def units_list(request, format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = models.Units.objects.all()
#         serializer = UnitsSerializer(snippets, many=True)
#         return Response(serializer.data)
#         #return JSONResponse(serializer.data)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = UnitsSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             #return JSONResponse(serializer.data, status=201)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             #return JSONResponse(serializer.errors, status=400)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# # @csrf_exempt
# def units_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = models.Units.objects.get(pk=pk)
#     except models.Units.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#         # return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = UnitsSerializer(snippet)
#         return Response(serializer.data)
#         # return JSONResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = UnitsSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#             # return JSONResponse(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             # return JSONResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         # return HttpResponse(status=204)
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class UnitstList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     """
#     List all snippets, or create a new snippet.
#     """

#     queryset = models.Units.objects.all()
#     serializer_class = UnitsSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     # Before adding mixins
#     # def get(self, request, format=None):
#     #     snippets = models.Units.objects.all()
#     #     serializer = UnitsSerializer(snippets, many=True)
#     #     return Response(serializer.data)

#     # def post(self, request, format=None):
#     #     serializer = UnitsSerializer(data=data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UnitsDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
    
#     queryset = models.Units.objects.all()
#     serializer_class = UnitsSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#     ## Pre mixins
#     # def get_object(self, pk):
#     #     try:
#     #         return models.Units.objects.get(pk=pk)
#     #     except models.Units.DoesNotExist:
#     #         raise Http404

#     # def get(self, request, pk, format=None):
#     #     snippet = self.get_object(pk)
#     #     serializer = UnitsSerializer(snippet)
#     #     return Response(serializer.data)

#     # def put(self, request, pk, format=None):
#     #     snippet = self.get_object(pk)
#     #     serializer = UnitsSerializer(snippet, data=request.DATA)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # def delete(self, request, pk, format=None):
#     #     snippet = self.get_object(pk)
#     #     snippet.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
