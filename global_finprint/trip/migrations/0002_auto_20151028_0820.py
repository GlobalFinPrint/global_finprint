# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpa',
            name='founded',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('C', 'Continental'), ('A', 'Atoll'), ('I', 'Island')], max_length=16),
        ),
    ]
