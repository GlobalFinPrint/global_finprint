# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-09-20 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0016_new_features'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('I', 'Island'), ('C', 'Continental'), ('A', 'Atoll'), ('O', 'Offshore Bank'), ('B', 'Barrier Reef'), ('V', 'Volcanic Island')], max_length=1),
        ),
    ]