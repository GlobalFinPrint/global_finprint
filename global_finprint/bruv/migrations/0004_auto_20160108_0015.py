# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0003_auto_20160107_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='habitat',
            field=models.CharField(max_length=1, choices=[('F', 'Forereef'), ('B', 'Backreef/Lagoon')], default='F'),
            preserve_default=False,
        ),
    ]
