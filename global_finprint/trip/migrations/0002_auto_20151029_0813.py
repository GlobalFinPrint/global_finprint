# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fishingrestrictions',
            name='description',
            field=models.CharField(max_length=48, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='protectionstatus',
            name='description',
            field=models.CharField(max_length=48, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reeftype',
            name='description',
            field=models.CharField(max_length=48, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sharkgearinuse',
            name='description',
            field=models.CharField(max_length=48, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mpacompliance',
            name='description',
            field=models.CharField(max_length=48),
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('I', 'Island'), ('C', 'Continental'), ('A', 'Atoll')], max_length=16),
        ),
    ]
