# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-07 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0050_auto_20170606_2120'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='attribute',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='animals',
        ),
        migrations.AddField(
            model_name='animal',
            name='projects',
            field=models.ManyToManyField(related_name='animals', to='annotation.Project'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='global_parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='annotation.GlobalAttribute'),
        ),
    ]
