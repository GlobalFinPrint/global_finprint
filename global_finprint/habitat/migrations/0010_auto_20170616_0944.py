# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-16 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0009_auto_20170606_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('I', 'Island'), ('C', 'Continental'), ('A', 'Atoll')], max_length=1),
        ),
    ]