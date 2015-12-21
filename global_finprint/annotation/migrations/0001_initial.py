# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import config.current_user
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bruv', '0002_auto_20151221_1315'),
        ('habitat', '0002_auto_20151221_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('rank', models.PositiveIntegerField()),
                ('group', models.CharField(max_length=1, choices=[('N', 'n/a'), ('T', 'Other target'), ('G', 'Groupers and jacks'), ('S', 'Shark'), ('R', 'Ray')])),
                ('common_name', models.CharField(max_length=100)),
                ('family', models.CharField(max_length=100)),
                ('genus', models.CharField(max_length=100)),
                ('species', models.CharField(max_length=100)),
                ('fishbase_key', models.IntegerField(blank=True, null=True)),
                ('sealifebase_key', models.IntegerField(blank=True, null=True)),
                ('region', models.ForeignKey(to='habitat.Region')),
            ],
        ),
        migrations.CreateModel(
            name='AnimalBehavior',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Annotator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('affiliation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('initial_observation_time', models.DateTimeField()),
                ('sex', models.CharField(max_length=1, choices=[('U', 'Unknown'), ('M', 'Male'), ('F', 'Female')], default='U')),
                ('stage', models.CharField(max_length=2, choices=[('U', 'Unknown'), ('JU', 'Juvenile'), ('AD', 'Adult')], default='U')),
                ('length', models.IntegerField(help_text='centimeters', null=True)),
                ('duration', models.PositiveIntegerField()),
                ('animal', models.ForeignKey(to='annotation.Animal')),
                ('behavior', models.ForeignKey(to='annotation.AnimalBehavior', null=True)),
                ('set', models.ForeignKey(to='bruv.Set')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObservationImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.FileField(upload_to='')),
                ('observation', models.ForeignKey(to='annotation.Observation')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.FileField(upload_to='')),
                ('set', models.ForeignKey(to='bruv.Set')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.FileField(upload_to='')),
                ('length', models.FloatField()),
                ('set', models.ForeignKey(to='bruv.Set')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoAnnotator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('annotator', models.ForeignKey(to='annotation.Annotator')),
                ('assigned_by', models.ForeignKey(related_name='assigned_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
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
        migrations.AlterUniqueTogether(
            name='animal',
            unique_together=set([('genus', 'species')]),
        ),
    ]
