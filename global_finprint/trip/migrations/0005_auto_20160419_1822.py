# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-04-19 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0004_auto_20160412_2234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('data_embargo_length', models.IntegerField(null=True)),
                ('code', models.CharField(default='FP', max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='data_embargo_termination',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trip.Source'),
        ),
    ]