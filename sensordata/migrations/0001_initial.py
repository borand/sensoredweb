# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField(blank=True)),
                ('format', models.CharField(max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device_name', models.CharField(max_length=225)),
                ('update_rate', models.DecimalField(default=1, verbose_name=b'Min. Update Interval [sec]', max_digits=15, decimal_places=3)),
                ('max_range', models.DecimalField(default=1, max_digits=15, decimal_places=3)),
                ('min_range', models.DecimalField(default=0, max_digits=15, decimal_places=3)),
                ('model_number', models.CharField(max_length=255, blank=True)),
                ('actuator', models.BooleanField(default=False)),
                ('protocol', models.CharField(max_length=255, verbose_name=b'Protocol', blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('callibration', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('transducer_type', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceGateway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'localhost', max_length=255, verbose_name=b'Name')),
                ('address', models.IPAddressField(default=b'127.0.0.1', verbose_name=b'Address')),
                ('port', models.IntegerField(default=8000, verbose_name=b'Port')),
                ('protocol', models.CharField(default=b'http', max_length=255, verbose_name=b'Protocol', blank=True)),
                ('url', models.URLField(blank=True)),
                ('mac_address', models.CharField(max_length=75, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('process_name', models.CharField(max_length=255, verbose_name=b'Process Name', blank=True)),
                ('process_pid', models.IntegerField(default=0, verbose_name=b'PID', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name=b'Description', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accept_from_gateway_only', models.BooleanField(default=False)),
                ('update_rate', models.DecimalField(default=1, verbose_name=b'Min. Update Interval [sec]', max_digits=15, decimal_places=3)),
                ('update_threshold', models.DecimalField(default=0, verbose_name=b'Min. change in value to accept update', max_digits=15, decimal_places=3)),
                ('active', models.BooleanField(default=True)),
                ('private', models.BooleanField(default=False)),
                ('serial_number', models.CharField(unique=True, max_length=255, verbose_name=b'Serial Number')),
                ('device', models.ForeignKey(to='sensordata.Device')),
                ('gateway', models.ForeignKey(to='sensordata.DeviceGateway')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('devices', models.ManyToManyField(to='sensordata.DeviceInstance')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area', models.TextField(default=b'None')),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('x_absolute', models.DecimalField(default=0, max_digits=10, decimal_places=3, blank=True)),
                ('y_absolute', models.DecimalField(default=0, max_digits=10, decimal_places=3, blank=True)),
                ('z_absolute', models.DecimalField(default=0, max_digits=10, decimal_places=3, blank=True)),
                ('reference_description', models.TextField(blank=True)),
                ('x_reference', models.DecimalField(default=0, max_digits=10, decimal_places=3, blank=True)),
                ('y_reference', models.DecimalField(default=0, max_digits=10, decimal_places=3, blank=True)),
                ('z_reference', models.DecimalField(default=0, max_digits=10, decimal_places=3, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'None', max_length=150)),
                ('url', models.URLField(max_length=750, blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(default=b'', max_length=255, blank=True)),
                ('content', models.TextField()),
                ('author', models.ForeignKey(related_name=b'Note', default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', 'title'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhysicalSignal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signal_name', models.CharField(default=b'None', max_length=25)),
                ('signal_description', models.CharField(max_length=30, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeStamp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_timestamp', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('measurement_timestamp', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'None', max_length=25)),
                ('symbol', models.CharField(max_length=30, blank=True)),
                ('system', models.CharField(max_length=8, blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='experiment',
            name='location',
            field=models.ForeignKey(to='sensordata.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deviceinstance',
            name='location',
            field=models.ForeignKey(to='sensordata.Location', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deviceinstance',
            name='physical_signal',
            field=models.ForeignKey(to='sensordata.PhysicalSignal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deviceinstance',
            name='user',
            field=models.ForeignKey(related_name=b'device_instance', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='device',
            name='manufacturer',
            field=models.ForeignKey(to='sensordata.Manufacturer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='device',
            name='units',
            field=models.ForeignKey(to='sensordata.Units'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('device_name', 'model_number')]),
        ),
        migrations.AddField(
            model_name='datavalue',
            name='data_timestamp',
            field=models.ForeignKey(to='sensordata.TimeStamp'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datavalue',
            name='device_instance',
            field=models.ForeignKey(to='sensordata.DeviceInstance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dataobject',
            name='data_timestamp',
            field=models.ForeignKey(to='sensordata.TimeStamp'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dataobject',
            name='device_instance',
            field=models.ForeignKey(to='sensordata.DeviceInstance'),
            preserve_default=True,
        ),
    ]
