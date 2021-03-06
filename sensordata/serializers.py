import time

from django.contrib.auth.models import User
from django.forms import widgets
from django.utils.log import getLogger

from rest_framework import serializers

from .models import Units, Location, Manufacturer, TimeStamp, DataValue,\
                    DeviceInstance, PhysicalSignal, Device, DeviceGateway

logger = getLogger("app")
#######################################################################################

class UserSerializer(serializers.ModelSerializer):
    device_instance = serializers.PrimaryKeyRelatedField(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'device_instance')

class UnitsSerializer(serializers.Serializer):
    """
    Adaptation of tutorial example to Units.
    based on http://django-rest-framework.org/tutorial/1-serialization.html
    """
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
 
    name   = serializers.CharField(max_length=25)
    symbol = serializers.CharField(max_length=30, blank=True)
    system = serializers.CharField(max_length=8, blank=True)
    notes  = serializers.CharField(blank=True)
 
    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.name = attrs.get('name', instance.name)
            instance.symbol = attrs.get('symbol', instance.symbol)
            instance.system = attrs.get('system', instance.system)
            instance.notes = attrs.get('notes', instance.notes)            
            return instance

        # Create new instance
        return Units(**attrs)

class UnitsSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Units

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'name', 'url', 'notes')

class TimeStampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeStamp
        fields = ('id', 'server_timestamp', 'measurement_timestamp')

class PhysicalSignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalSignal

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device

class DeviceGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceGateway
        # fields = ('id', 'name', 'address','port','protocol','url','mac_address','active','process_name','process_pid','description')

class DeviceInstanceSerializer(serializers.ModelSerializer):
    #user = serializers.Field(source='user.username')
    #device = serializers.Field(source='device.device_name')
    class Meta:
        model = DeviceInstance
        # fields = ('id','user', 'device','gateway','accept_from_gateway_only',\
        #     'location','physical_signal','update_rate','active','private','serial_number')
        # fields = ('id','user', 'accept_from_gateway_only','update_rate','active','private','serial_number')

class DataValueSerializer(serializers.ModelSerializer):
    # device_instance = serializers.Field(source='device_instance')
    class Meta:
        model = DataValue
        # fields = ('data_timestamp', 'device_instance','value')

class DataValuePairSerializer(serializers.ModelSerializer):
    data_timestamp  = serializers.Field(source='data_timestamp.measurement_timestamp')
    # device_instance = serializers.Field(source='device_instance.serial_number')
    # device = serializers.Field(source='device_instance.device')
    value = serializers.Field(source='get_value_pair')
    class Meta:
        model = DataValue
        # fields = ('data_timestamp','value')
        fields = ('value',)

class DataValuePairSerializer2(serializers.Serializer):
    """
    Adaptation of tutorial example to Units.
    based on http://django-rest-framework.org/tutorial/1-serialization.html
    """
 
    data_timestamp = serializers.DateTimeField()
    value          = serializers.FloatField()

    @property
    def data(self):

        to = time.time()
        logger.debug("Found %d items matching criteria " % self.object.count())
        values_list = self.object.values_list('data_timestamp__measurement_timestamp','value')    
        v = self.object.values_list('value',flat=True)
        t = self.object.values_list('data_timestamp__measurement_timestamp',flat=True)
        logger.debug("Making the list        = %.3f" % (time.time() - to))

        logger.debug("Preparing array for json transmision")
        data = []
        for data_pt in values_list:        
            data.append([time.mktime(data_pt[0].timetuple()),data_pt[1]])

        logger.debug("Making value pair list = %.3f" % (time.time() - to))
        return data

