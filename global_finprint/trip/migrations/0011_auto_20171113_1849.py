# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-13 18:49
from __future__ import unicode_literals

import config.current_user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0010_trip_last_modified_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='user',
            field=models.ForeignKey(default=config.current_user.get_current_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]