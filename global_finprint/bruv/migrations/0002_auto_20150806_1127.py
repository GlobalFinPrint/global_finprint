# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('habitat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trip', '0002_auto_20150806_1127'),
        ('bruv', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('drop_time', models.DateTimeField()),
                ('collection_time', models.DateTimeField(null=True)),
                ('time_bait_gone', models.DateTimeField(null=True)),
                ('depth', models.FloatField(null=True)),
                ('benthic', models.ForeignKey(to='habitat.Benthic')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='drop',
            name='benthic',
        ),
        migrations.RemoveField(
            model_name='drop',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='drop',
            name='reef',
        ),
        migrations.RemoveField(
            model_name='drop',
            name='trip',
        ),
        migrations.RemoveField(
            model_name='drop',
            name='user',
        ),
        migrations.RemoveField(
            model_name='environmentmeasure',
            name='deployment',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='bruv',
        ),
        migrations.RemoveField(
            model_name='observation',
            name='deployment',
        ),
        migrations.RemoveField(
            model_name='siteimage',
            name='site',
        ),
        migrations.RemoveField(
            model_name='video',
            name='deployment',
        ),
        migrations.AddField(
            model_name='equipment',
            name='bait',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipment',
            name='bruv_frame',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='length',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='camera',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='observationimage',
            name='name',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='observedfish',
            name='sex',
            field=models.CharField(max_length=1, choices=[('M', 'Male'), ('U', 'Unknown'), ('F', 'Female')]),
        ),
        migrations.AlterField(
            model_name='siteimage',
            name='name',
            field=models.FileField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.FileField(upload_to=''),
        ),
        migrations.DeleteModel(
            name='Drop',
        ),
        migrations.AddField(
            model_name='set',
            name='equipment',
            field=models.ForeignKey(to='bruv.Equipment'),
        ),
        migrations.AddField(
            model_name='set',
            name='reef',
            field=models.ForeignKey(to='trip.Reef'),
        ),
        migrations.AddField(
            model_name='set',
            name='trip',
            field=models.ForeignKey(to='trip.Trip'),
        ),
        migrations.AddField(
            model_name='set',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='environmentmeasure',
            name='set',
            field=models.ForeignKey(to='bruv.Set', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='set',
            field=models.ForeignKey(to='bruv.Set', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='siteimage',
            name='set',
            field=models.ForeignKey(to='bruv.Set', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='set',
            field=models.ForeignKey(to='bruv.Set', default=1),
            preserve_default=False,
        ),
    ]
