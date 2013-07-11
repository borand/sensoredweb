# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Units'
        db.create_table(u'sensordata_units', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='None', max_length=25)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sensordata', ['Units'])

        # Adding model 'Manufacturer'
        db.create_table(u'sensordata_manufacturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='None', max_length=150)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=750, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sensordata', ['Manufacturer'])

        # Adding model 'TimeStamp'
        db.create_table(u'sensordata_timestamp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('measurement_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'sensordata', ['TimeStamp'])

        # Adding model 'PhysicalSignal'
        db.create_table(u'sensordata_physicalsignal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signal_name', self.gf('django.db.models.fields.CharField')(default='None', max_length=25)),
            ('signal_description', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'sensordata', ['PhysicalSignal'])

        # Adding model 'Device'
        db.create_table(u'sensordata_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.Manufacturer'])),
            ('device_name', self.gf('django.db.models.fields.CharField')(max_length=225)),
            ('units', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.Units'])),
            ('update_rate', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=15, decimal_places=3)),
            ('max_range', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=15, decimal_places=3)),
            ('min_range', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=3)),
            ('model_number', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('actuator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('callibration', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transducer_type', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'sensordata', ['Device'])

        # Adding unique constraint on 'Device', fields ['device_name', 'model_number']
        db.create_unique(u'sensordata_device', ['device_name', 'model_number'])

        # Adding model 'DeviceGateway'
        db.create_table(u'sensordata_devicegateway', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='localhost', max_length=255)),
            ('address', self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15)),
            ('port', self.gf('django.db.models.fields.IntegerField')(default=8000)),
            ('protocol', self.gf('django.db.models.fields.CharField')(default='http', max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('mac_address', self.gf('django.db.models.fields.CharField')(max_length=75, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('process_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('process_pid', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'sensordata', ['DeviceGateway'])

        # Adding model 'Location'
        db.create_table(u'sensordata_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.TextField')(default='None')),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('x_absolute', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3, blank=True)),
            ('y_absolute', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3, blank=True)),
            ('z_absolute', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3, blank=True)),
            ('reference_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('x_reference', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3, blank=True)),
            ('y_reference', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3, blank=True)),
            ('z_reference', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3, blank=True)),
        ))
        db.send_create_signal(u'sensordata', ['Location'])

        # Adding model 'DeviceInstance'
        db.create_table(u'sensordata_deviceinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.Device'])),
            ('gateway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.DeviceGateway'])),
            ('accept_from_gateway_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.Location'], null=True)),
            ('physical_signal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.PhysicalSignal'])),
            ('update_rate', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=15, decimal_places=3)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'sensordata', ['DeviceInstance'])

        # Adding model 'DataValue'
        db.create_table(u'sensordata_datavalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_timestamp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.TimeStamp'])),
            ('device_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.DeviceInstance'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'sensordata', ['DataValue'])

        # Adding model 'Note'
        db.create_table(u'sensordata_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=255, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='Note', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'sensordata', ['Note'])

        # Adding model 'DataObject'
        db.create_table(u'sensordata_dataobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_timestamp', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.TimeStamp'])),
            ('device_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.DeviceInstance'])),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'sensordata', ['DataObject'])


    def backwards(self, orm):
        # Removing unique constraint on 'Device', fields ['device_name', 'model_number']
        db.delete_unique(u'sensordata_device', ['device_name', 'model_number'])

        # Deleting model 'Units'
        db.delete_table(u'sensordata_units')

        # Deleting model 'Manufacturer'
        db.delete_table(u'sensordata_manufacturer')

        # Deleting model 'TimeStamp'
        db.delete_table(u'sensordata_timestamp')

        # Deleting model 'PhysicalSignal'
        db.delete_table(u'sensordata_physicalsignal')

        # Deleting model 'Device'
        db.delete_table(u'sensordata_device')

        # Deleting model 'DeviceGateway'
        db.delete_table(u'sensordata_devicegateway')

        # Deleting model 'Location'
        db.delete_table(u'sensordata_location')

        # Deleting model 'DeviceInstance'
        db.delete_table(u'sensordata_deviceinstance')

        # Deleting model 'DataValue'
        db.delete_table(u'sensordata_datavalue')

        # Deleting model 'Note'
        db.delete_table(u'sensordata_note')

        # Deleting model 'DataObject'
        db.delete_table(u'sensordata_dataobject')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sensordata.dataobject': {
            'Meta': {'object_name': 'DataObject'},
            'data_timestamp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.TimeStamp']"}),
            'device_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.DeviceInstance']"}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'sensordata.datavalue': {
            'Meta': {'object_name': 'DataValue'},
            'data_timestamp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.TimeStamp']"}),
            'device_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.DeviceInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'sensordata.device': {
            'Meta': {'unique_together': "(('device_name', 'model_number'),)", 'object_name': 'Device'},
            'actuator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'callibration': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'device_name': ('django.db.models.fields.CharField', [], {'max_length': '225'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.Manufacturer']"}),
            'max_range': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '15', 'decimal_places': '3'}),
            'min_range': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '3'}),
            'model_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'transducer_type': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'units': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.Units']"}),
            'update_rate': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '15', 'decimal_places': '3'})
        },
        u'sensordata.devicegateway': {
            'Meta': {'object_name': 'DeviceGateway'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'localhost'", 'max_length': '255'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '8000'}),
            'process_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'process_pid': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'default': "'http'", 'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'sensordata.deviceinstance': {
            'Meta': {'object_name': 'DeviceInstance'},
            'accept_from_gateway_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.Device']"}),
            'gateway': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.DeviceGateway']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.Location']", 'null': 'True'}),
            'physical_signal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.PhysicalSignal']"}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'update_rate': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '15', 'decimal_places': '3'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['auth.User']"})
        },
        u'sensordata.location': {
            'Meta': {'object_name': 'Location'},
            'area': ('django.db.models.fields.TextField', [], {'default': "'None'"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'reference_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'x_absolute': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'x_reference': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'y_absolute': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'y_reference': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'z_absolute': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'z_reference': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'})
        },
        u'sensordata.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '150'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '750', 'blank': 'True'})
        },
        u'sensordata.note': {
            'Meta': {'ordering': "['-created_at', 'title']", 'object_name': 'Note'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'Note'", 'to': u"orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'sensordata.physicalsignal': {
            'Meta': {'object_name': 'PhysicalSignal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signal_description': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'signal_name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '25'})
        },
        u'sensordata.timestamp': {
            'Meta': {'object_name': 'TimeStamp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'server_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        },
        u'sensordata.units': {
            'Meta': {'object_name': 'Units'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'None'", 'max_length': '25'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'})
        }
    }

    complete_apps = ['sensordata']