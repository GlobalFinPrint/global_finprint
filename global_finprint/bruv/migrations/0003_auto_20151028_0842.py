# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0002_auto_20151028_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(choices=[('JU', 'Juvenile'), ('U', 'Unknown'), ('AD', 'Adult')], default='U', max_length=2),
        ),
    ]
