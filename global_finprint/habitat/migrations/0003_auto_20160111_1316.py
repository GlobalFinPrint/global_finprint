# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-11 21:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0002_auto_20160111_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='code',
            field=models.CharField(help_text='3166-1 alpha-2, if applicable.', max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='reef',
            name='code',
            field=models.CharField(help_text='Must be unique for reef site.', max_length=1),
        ),
        migrations.AlterField(
            model_name='reef',
            name='name',
            field=models.CharField(help_text='Must be unique for reef site.', max_length=100),
        ),
        migrations.AlterField(
            model_name='site',
            name='code',
            field=models.CharField(help_text='Must be unique for site location.', max_length=2),
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(help_text='Must be unique for site location.', max_length=100),
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.CharField(choices=[('A', 'Atoll'), ('C', 'Continental'), ('I', 'Island')], max_length=16),
        ),
    ]
