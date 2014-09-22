# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensordata', '0002_timestamp_measurement_timestamp_ms'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timestamp',
            name='measurement_timestamp_ms',
        ),
        migrations.AddField(
            model_name='timestamp',
            name='measurement_timestamp_sec',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
