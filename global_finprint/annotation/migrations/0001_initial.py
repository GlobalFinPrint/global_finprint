# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import config.current_user
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bruv', '0001_initial'),
        ('habitat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('rank', models.PositiveIntegerField()),
                ('common_name', models.CharField(max_length=100)),
                ('family', models.CharField(max_length=100)),
                ('genus', models.CharField(max_length=100)),
                ('species', models.CharField(max_length=100)),
                ('fishbase_key', models.IntegerField(null=True, blank=True)),
                ('sealifebase_key', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalBehavior',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalGroup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Annotator',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('affiliation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('initial_observation_time', models.DateTimeField()),
                ('sex', models.CharField(default='U', choices=[('U', 'Unknown'), ('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('stage', models.CharField(default='U', choices=[('JU', 'Juvenile'), ('U', 'Unknown'), ('AD', 'Adult')], max_length=2)),
                ('length', models.IntegerField(help_text='centimeters', null=True)),
                ('duration', models.PositiveIntegerField()),
                ('animal', models.ForeignKey(to='annotation.Animal')),
                ('behavior', models.ForeignKey(null=True, to='annotation.AnimalBehavior')),
                ('set', models.ForeignKey(to='bruv.Set')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObservationImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.FileField(upload_to='')),
                ('observation', models.ForeignKey(to='annotation.Observation')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.FileField(upload_to='')),
                ('set', models.ForeignKey(to='bruv.Set')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.FileField(upload_to='')),
                ('length', models.FloatField()),
                ('set', models.ForeignKey(to='bruv.Set')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoAnnotator',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('annotator', models.ForeignKey(to='annotation.Annotator')),
                ('assigned_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='assigned_by')),
                ('user', models.ForeignKey(default=config.current_user.get_current_user, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(to='annotation.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='siteimage',
            name='video',
            field=models.ForeignKey(to='annotation.Video'),
        ),
        migrations.AddField(
            model_name='observationimage',
            name='video',
            field=models.ForeignKey(to='annotation.Video'),
        ),
        migrations.AddField(
            model_name='observation',
            name='video_annotator',
            field=models.ForeignKey(to='annotation.VideoAnnotator'),
        ),
        migrations.AddField(
            model_name='animal',
            name='group',
            field=models.ForeignKey(to='annotation.AnimalGroup'),
        ),
        migrations.AddField(
            model_name='animal',
            name='regions',
            field=models.ManyToManyField(to='habitat.Region'),
        ),
        migrations.AlterUniqueTogether(
            name='animal',
            unique_together=set([('genus', 'species')]),
        ),
    ]
