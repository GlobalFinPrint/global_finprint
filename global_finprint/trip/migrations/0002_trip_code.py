# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-14 16:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='code',
            field=models.CharField(default='FP_2015', max_length=32),
            preserve_default=False,
        ),
    ]
