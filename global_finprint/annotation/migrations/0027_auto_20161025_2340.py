# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-25 23:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0026_master_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterrecord',
            name='set',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bruv.Set'),
        ),
    ]