# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-19 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0006_auto_20160719_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='arm_length',
            field=models.PositiveIntegerField(help_text='centimeters', null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='camera_height',
            field=models.PositiveIntegerField(help_text='centimeters', null=True),
        ),
    ]