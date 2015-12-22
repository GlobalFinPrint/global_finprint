# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import config.current_user
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('habitat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('association', models.CharField(max_length=100)),
                ('lead', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('boat', models.CharField(max_length=100, null=True, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', models.ForeignKey(to='habitat.Location')),
                ('team', models.ForeignKey(to='trip.Team')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
