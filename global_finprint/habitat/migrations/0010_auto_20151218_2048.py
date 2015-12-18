# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0009_auto_20151218_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('I', 'Island'), ('C', 'Continental'), ('A', 'Atoll')], max_length=16),
        ),
    ]
