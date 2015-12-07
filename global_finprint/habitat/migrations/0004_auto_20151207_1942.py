# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0003_auto_20151207_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('A', 'Atoll'), ('C', 'Continental'), ('I', 'Island')], max_length=16),
        ),
    ]
