# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-11 03:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20160412_2234'),
        ('habitat', '0007_auto_20160705_0342'),
        ('trip', '0008_source_legacy'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlannedSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planned_start_date', models.DateField(blank=True, null=True)),
                ('planned_end_date', models.DateField(blank=True, null=True)),
                ('funder', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('P', 'In Progress'), ('C', 'Completed'), ('W', 'Wishlist'), ('F', 'Forthcoming')], max_length=1)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habitat.Location')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='habitat.Site')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Team')),
                ('trip', models.ManyToManyField(to='trip.Trip')),
            ],
        ),
    ]
