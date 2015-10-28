# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_auto_20151028_0820'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fishingrestrictions',
            options={'verbose_name_plural': 'Fishing restrictions'},
        ),
        migrations.AlterModelOptions(
            name='mpa',
            options={'verbose_name_plural': 'MPAs', 'verbose_name': 'MPA'},
        ),
        migrations.AlterModelOptions(
            name='mpacompliance',
            options={'verbose_name_plural': 'MPA compliance', 'verbose_name': 'MPA compliance'},
        ),
        migrations.AlterModelOptions(
            name='mpaisolation',
            options={'verbose_name_plural': 'MPA isolation', 'verbose_name': 'MPA isolation'},
        ),
        migrations.AlterModelOptions(
            name='protectionstatus',
            options={'verbose_name_plural': 'Protection status'},
        ),
        migrations.AlterModelOptions(
            name='sharkgearinuse',
            options={'verbose_name_plural': 'Shark gear in use'},
        ),
        migrations.AlterField(
            model_name='sharkgearinuse',
            name='type',
            field=models.CharField(max_length=24),
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('A', 'Atoll'), ('I', 'Island'), ('C', 'Continental')], max_length=16),
        ),
    ]
