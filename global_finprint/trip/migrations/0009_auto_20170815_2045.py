# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-15 20:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0008_source_legacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='code',
            field=models.CharField(blank=True, db_index=True, help_text='[source code]_[year]_[loc code]_xx', max_length=32, null=True, unique=True),
        ),
    ]
