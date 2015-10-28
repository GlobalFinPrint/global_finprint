# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(default='U', choices=[('AD', 'Adult'), ('U', 'Unknown'), ('JU', 'Juvenile')], max_length=2),
        ),
    ]
