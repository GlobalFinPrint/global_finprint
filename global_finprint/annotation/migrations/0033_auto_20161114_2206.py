# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-14 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0032_auto_20161114_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]