# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-09-20 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_auto_20170815_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plannedsite',
            name='status',
            field=models.CharField(choices=[('F', 'Forthcoming'), ('C', 'Completed'), ('P', 'In Progress'), ('W', 'Wishlist')], max_length=1),
        ),
    ]
