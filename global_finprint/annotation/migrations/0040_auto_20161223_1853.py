# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-23 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0039_auto_20161223_1837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videofile',
            old_name='source_folder',
            new_name='source',
        ),
    ]
