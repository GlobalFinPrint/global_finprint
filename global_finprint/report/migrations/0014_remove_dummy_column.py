# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-09-20 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0013_dummy_column'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='description',
            name='test_column',
        ),
        migrations.AlterField(
            model_name='plannedsite',
            name='status',
            field=models.CharField(choices=[('C', 'Completed'), ('W', 'Wishlist'), ('P', 'In Progress'), ('F', 'Forthcoming')], max_length=1),
        ),
    ]
