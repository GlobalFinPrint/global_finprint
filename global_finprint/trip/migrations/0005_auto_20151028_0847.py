# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0004_auto_20151028_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpaisolation',
            name='type',
            field=models.CharField(max_length=24),
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(max_length=16, choices=[('C', 'Continental'), ('I', 'Island'), ('A', 'Atoll')]),
        ),
    ]
