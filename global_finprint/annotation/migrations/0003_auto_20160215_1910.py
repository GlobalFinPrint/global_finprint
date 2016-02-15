# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-15 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0002_auto_20160201_0329'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='external_parasites',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='observation',
            name='gear_fouled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='observation',
            name='gear_on_animal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='observation',
            name='tag',
            field=models.CharField(choices=[('D', 'Dart tag'), ('R', 'Roto tag'), ('O', 'Other'), ('N', 'None')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='videoannotator',
            name='status',
            field=models.CharField(choices=[('R', 'Ready for review'), ('I', 'In progress'), ('D', 'Disabled'), ('N', 'Not started'), ('C', 'Competed')], default='N', max_length=1),
        ),
    ]