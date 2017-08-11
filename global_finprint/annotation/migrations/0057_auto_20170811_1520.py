# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-11 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0056_auto_20170724_2033'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventmeasurable',
            unique_together=set([('event', 'measurable')]),
        ),
        migrations.AlterUniqueTogether(
            name='mastereventmeasurable',
            unique_together=set([('master_event', 'measurable')]),
        ),
    ]
