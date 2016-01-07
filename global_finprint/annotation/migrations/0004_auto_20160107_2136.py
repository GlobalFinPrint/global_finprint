# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0003_auto_20160106_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoannotator',
            name='status',
            field=models.CharField(default='N', choices=[('C', 'Competed'), ('N', 'Not started'), ('I', 'In progress')], max_length=1),
        ),
    ]
