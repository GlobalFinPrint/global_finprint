# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-18 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0015_data_migrate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]