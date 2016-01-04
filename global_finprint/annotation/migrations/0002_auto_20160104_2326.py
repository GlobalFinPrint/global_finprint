# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('annotation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('affiliation', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='annotator',
            name='email',
        ),
        migrations.RemoveField(
            model_name='annotator',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='annotator',
            name='last_name',
        ),
        migrations.AddField(
            model_name='annotator',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='observation',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], default='U', max_length=1),
        ),
        migrations.AlterField(
            model_name='observation',
            name='stage',
            field=models.CharField(choices=[('AD', 'Adult'), ('JU', 'Juvenile'), ('U', 'Unknown')], default='U', max_length=2),
        ),
        migrations.AlterField(
            model_name='videoannotator',
            name='assigned_by',
            field=models.ForeignKey(to='annotation.Lead', related_name='assigned_by'),
        ),
    ]
