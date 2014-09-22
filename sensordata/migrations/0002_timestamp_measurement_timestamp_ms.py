# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensordata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timestamp',
            name='measurement_timestamp_ms',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
