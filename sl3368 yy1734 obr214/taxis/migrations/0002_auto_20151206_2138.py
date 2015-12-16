# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxipickups',
            name='dropoff_latitude',
            field=models.FloatField(null=True, verbose_name=b'Drop Off Longitude', blank=True),
        ),
        migrations.AlterField(
            model_name='taxipickups',
            name='dropoff_longitude',
            field=models.FloatField(null=True, verbose_name=b'Drop Off Longitude', blank=True),
        ),
        migrations.AlterField(
            model_name='taxipickups',
            name='pickup_latitude',
            field=models.FloatField(null=True, verbose_name=b'Pick Up Latitude', blank=True),
        ),
        migrations.AlterField(
            model_name='taxipickups',
            name='pickup_longitude',
            field=models.FloatField(null=True, verbose_name=b'Pick Up Longitude', blank=True),
        ),
    ]
