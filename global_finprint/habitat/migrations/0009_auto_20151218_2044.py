# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0008_auto_20151218_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(max_length=16, choices=[('I', 'Island'), ('A', 'Atoll'), ('C', 'Continental')]),
        ),
    ]
