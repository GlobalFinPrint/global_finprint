# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-04-16 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0060_auto_20171129_0122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventmeasurable',
            name='create_datetime',
        ),
        migrations.RemoveField(
            model_name='eventmeasurable',
            name='last_modified_by',
        ),
        migrations.RemoveField(
            model_name='eventmeasurable',
            name='last_modified_datetime',
        ),
        migrations.RemoveField(
            model_name='eventmeasurable',
            name='user',
        ),
        migrations.RemoveField(
            model_name='mastereventmeasurable',
            name='create_datetime',
        ),
        migrations.RemoveField(
            model_name='mastereventmeasurable',
            name='last_modified_by',
        ),
        migrations.RemoveField(
            model_name='mastereventmeasurable',
            name='last_modified_datetime',
        ),
        migrations.RemoveField(
            model_name='mastereventmeasurable',
            name='user',
        ),
    ]