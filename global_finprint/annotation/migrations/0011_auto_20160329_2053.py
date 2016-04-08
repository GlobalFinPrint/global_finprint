# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-29 20:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('annotation', '0010_auto_20160315_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotationState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='videoannotator',
            name='status',
            field=models.ForeignKey(default=1,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    to='annotation.AnnotationState'),
        ),
    ]