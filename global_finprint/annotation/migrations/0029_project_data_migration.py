# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-11 19:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def create_default_project(apps, schema_editor):
    Project = apps.get_model('annotation', 'Project')
    User = apps.get_model('auth', 'User')
    db_alias = schema_editor.connection.alias
    try:
        User.objects.using(db_alias).get(pk=1)
        Project.objects.using(db_alias).bulk_create([
            Project(id=1, name='Global FinPrint Project', user_id=1),
        ])
    except:
        pass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('annotation', '0028_auto_20161111_1911'),
    ]

    operations = [
        migrations.RunPython(create_default_project),
    ]
