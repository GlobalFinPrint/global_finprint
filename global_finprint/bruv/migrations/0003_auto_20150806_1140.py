# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0002_auto_20150806_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observedfish',
            name='sex',
            field=models.CharField(max_length=1, choices=[('U', 'Unknown'), ('F', 'Female'), ('M', 'Male')]),
        ),
        migrations.AlterField(
            model_name='observedfish',
            name='stage',
            field=models.TextField(max_length=2, choices=[('U', 'Unknown'), ('AD', 'Adult'), ('JU', 'Juvenile')], default='AD'),
            preserve_default=False,
        ),
    ]
