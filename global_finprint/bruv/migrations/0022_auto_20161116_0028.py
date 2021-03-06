# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-16 00:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0008_auto_20161116_0027'),
        ('bruv', '0021_auto_20161115_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='substrate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='habitat.Substrate'),
        ),
        migrations.AddField(
            model_name='set',
            name='substrate_complexity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='habitat.SubstrateComplexity'),
        ),
    ]
