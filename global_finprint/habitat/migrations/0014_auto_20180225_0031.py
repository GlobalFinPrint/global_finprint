# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-02-25 00:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0013_auto_20170815_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('I', 'Island'), ('O', 'Offshore Bank'), ('B', 'Barrier Reef'), ('A', 'Atoll'), ('C', 'Continental'), ('V', 'Volcanic Island')], max_length=1),
        ),
    ]
