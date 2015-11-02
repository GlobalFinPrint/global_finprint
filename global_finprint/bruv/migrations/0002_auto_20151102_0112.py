# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import config.current_user


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bruv', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotator',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('email', models.EmailField(unique=True, max_length=100)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('affiliation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VideoAnnotator',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('annotator', models.ForeignKey(to='bruv.Annotator')),
                ('assigned_by', models.ForeignKey(related_name='assigned_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=config.current_user.get_current_user)),
                ('video', models.ForeignKey(to='bruv.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='observation',
            name='observer',
        ),
        migrations.AlterField(
            model_name='environmentmeasure',
            name='current_direction',
            field=models.CharField(max_length=2, help_text='compass direction', choices=[('SW', 'Southwest'), ('W', 'West'), ('NW', 'Northwest'), ('SE', 'Southeast'), ('S', 'South'), ('N', 'North'), ('NE', 'Northeast'), ('E', 'East')], null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='bait_container',
            field=models.CharField(max_length=1, choices=[('C', 'Cage'), ('B', 'Bag')], default='C'),
        ),
        migrations.AlterField(
            model_name='set',
            name='visibility',
            field=models.CharField(max_length=3, choices=[('1', '1'), ('14', '14'), ('13', '13'), ('7', '7'), ('6', '6'), ('3', '3'), ('>15', '>15'), ('12', '12'), ('9', '9'), ('5', '5'), ('4', '4'), ('11', '11'), ('2', '2'), ('15', '15'), ('10', '10'), ('8', '8')]),
        ),
        migrations.DeleteModel(
            name='Observer',
        ),
        migrations.AddField(
            model_name='observation',
            name='video_annotator',
            field=models.ForeignKey(to='bruv.VideoAnnotator', default=1),
            preserve_default=False,
        ),
    ]
