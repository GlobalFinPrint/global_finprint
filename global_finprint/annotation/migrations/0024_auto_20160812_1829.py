# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-12 18:29
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0023_auto_20160810_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='raw_import_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]