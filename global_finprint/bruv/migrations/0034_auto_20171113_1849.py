# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-13 18:49
from __future__ import unicode_literals

import config.current_user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0033_auto_20171109_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bait',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='set',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
