# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-14 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0031_auto_20161111_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterobservation',
            name='observation_time',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='observation',
            name='observation_time',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]