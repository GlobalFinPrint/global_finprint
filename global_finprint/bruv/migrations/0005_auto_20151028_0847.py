# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0004_auto_20151028_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(default='U', max_length=2, choices=[('U', 'Unknown'), ('JU', 'Juvenile'), ('AD', 'Adult')]),
        ),
    ]
