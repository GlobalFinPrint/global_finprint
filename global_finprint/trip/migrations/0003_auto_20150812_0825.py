# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trip', '0002_auto_20150806_1127'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('create_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('association', models.CharField(max_length=100)),
                ('lead', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='reef',
            name='type',
            field=models.CharField(max_length=100, default='forereef'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='boundary',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True),
        ),
        migrations.AlterField(
            model_name='reef',
            name='boundary',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True),
        ),
        migrations.AlterField(
            model_name='reef',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='boundary',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='boat',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trip',
            name='type',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='trip',
            name='team',
            field=models.ForeignKey(to='trip.Team', default=1),
            preserve_default=False,
        ),
    ]
