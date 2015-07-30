# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bruv', '0002_auto_20150730_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservationImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('site', models.ForeignKey(to='bruv.Site')),
                ('video', models.ForeignKey(to='bruv.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='image',
            name='video',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='image',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.AddField(
            model_name='observationimage',
            name='observation',
            field=models.ForeignKey(to='bruv.Observation'),
        ),
        migrations.AddField(
            model_name='observationimage',
            name='video',
            field=models.ForeignKey(to='bruv.Video'),
        ),
    ]
