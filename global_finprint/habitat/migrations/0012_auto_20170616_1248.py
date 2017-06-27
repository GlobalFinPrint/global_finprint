# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-16 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0011_auto_20170616_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('A', 'Atoll'), ('I', 'Island'), ('C', 'Continental')], max_length=1),
        ),
    ]