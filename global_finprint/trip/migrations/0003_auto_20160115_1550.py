# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_trip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='code',
            field=models.CharField(help_text='FP_[year]_[loc code]_xx', max_length=32),
        ),
    ]