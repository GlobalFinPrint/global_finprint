# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_auto_20151028_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='mpacompliance',
            name='description',
            field=models.CharField(default='', max_length=24),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('A', 'Atoll'), ('C', 'Continental'), ('I', 'Island')], max_length=16),
        ),
    ]
