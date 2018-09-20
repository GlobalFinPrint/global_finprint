# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-09-20 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0019_dummy_column'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('O', 'Offshore Bank'), ('I', 'Island'), ('A', 'Atoll'), ('V', 'Volcanic Island'), ('C', 'Continental'), ('B', 'Barrier Reef')], max_length=1),
        ),
    ]
