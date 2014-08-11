# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Experiment'
        db.create_table(u'sensordata_experiment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sensordata.Location'], null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'sensordata', ['Experiment'])

        # Adding M2M table for field devices on 'Experiment'
        m2m_table_name = db.shorten_name(u'sensordata_experiment_devices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('experiment', models.ForeignKey(orm[u'sensordata.experiment'], null=False)),
            ('deviceinstance', models.ForeignKey(orm[u'sensordata.deviceinstance'], null=False))
        ))
        db.create_unique(m2m_table_name, ['experiment_id', 'deviceinstance_id'])

        # Adding field 'DeviceInstance.update_threshold'
        db.add_column(u'sensordata_deviceinstance', 'update_threshold',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=15, decimal_places=3),
                      keep_default=False)

        # Adding unique constraint on 'DeviceInstance', fields ['serial_number']
        db.create_unique(u'sensordata_deviceinstance', ['serial_number'])


    def backwards(self, orm):
        # Removing unique constraint on 'DeviceInstance', fields ['serial_number']
        db.delete_unique(u'sensordata_deviceinstance', ['serial_number'])

        # Deleting model 'Experiment'
        db.delete_table(u'sensordata_experiment')

        # Removing M2M table for field devices on 'Experiment'
        db.delete_table(db.shorten_name(u'sensordata_experiment_devices'))

        # Deleting field 'DeviceInstance.update_threshold'
        db.delete_column(u'sensordata_deviceinstance', 'update_threshold')


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
            'serial_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'update_rate': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '15', 'decimal_places': '3'}),
            'update_threshold': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '15', 'decimal_places': '3'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'device_instance'", 'to': u"orm['auth.User']"})
        },
        u'sensordata.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'devices': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sensordata.DeviceInstance']", 'symmetrical': 'False'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sensordata.Location']", 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
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