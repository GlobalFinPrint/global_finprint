# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-02 00:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_auto_20160201_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='code',
            field=models.CharField(blank=True, help_text='FP_[year]_[loc code]_xx', max_length=32, null=True, unique=True),
        ),
    ]
