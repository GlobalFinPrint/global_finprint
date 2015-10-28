# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0003_auto_20151028_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(choices=[('U', 'Unknown'), ('M', 'Male'), ('F', 'Female')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(choices=[('U', 'Unknown'), ('AD', 'Adult'), ('JU', 'Juvenile')], default='U', max_length=2),
        ),
    ]
