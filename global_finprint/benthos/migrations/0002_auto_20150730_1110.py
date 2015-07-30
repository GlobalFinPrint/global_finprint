# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('benthos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benthic',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.ForeignKey(to='benthos.BenthicCategory')),
            ],
        ),
        migrations.CreateModel(
            name='BenthicCommunity',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Substrate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='benthic',
            name='community',
            field=models.ForeignKey(to='benthos.BenthicCommunity'),
        ),
        migrations.AddField(
            model_name='benthic',
            name='substrate',
            field=models.ForeignKey(to='benthos.Substrate'),
        ),
    ]
