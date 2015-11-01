# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='substrate',
            name='name',
        ),
        migrations.AddField(
            model_name='substrate',
            name='type',
            field=models.CharField(max_length=24, unique=True, default=''),
            preserve_default=False,
        ),
    ]
