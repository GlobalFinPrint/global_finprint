# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0007_auto_20151218_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(max_length=16, choices=[('I', 'Island'), ('C', 'Continental'), ('A', 'Atoll')]),
        ),
    ]
