from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import serializers
from .models import Units, Manufacturer, TimeStamp, DataValue,\
                    DeviceInstance, PhysicalSignal, Device, DeviceGateway


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
        fields = ('id', 'name', 'address','port','protocol','url','mac_address','active','process_name','process_pid','description')

class DataValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataValue
        fields = ('data_timestamp', 'device_instance','value')

class DeviceInstanceSerializer(serializers.ModelSerializer):
    user = serializers.Field(source='user.username')
    class Meta:
        model = DeviceInstance
        # fields = ('id','user', 'device','gateway','accept_from_gateway_only',\
        #     'location','physical_signal','update_rate','active','private','serial_number')
        fields = ('id','user', 'accept_from_gateway_only','update_rate','active','private','serial_number')
