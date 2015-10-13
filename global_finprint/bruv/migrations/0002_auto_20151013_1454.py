# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='common_name',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='observedanimal',
            name='sex',
            field=models.CharField(choices=[('F', 'Female'), ('U', 'Unknown'), ('M', 'Male')], max_length=1),
        ),
    ]
