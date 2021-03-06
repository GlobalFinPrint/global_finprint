# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-12 23:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160412_2234'),
        ('annotation', '0013_auto_20160412_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observations_created', to='core.FinprintUser'),
        ),
        migrations.AddField(
            model_name='observation',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observations_updated', to='core.FinprintUser'),
        ),
    ]
