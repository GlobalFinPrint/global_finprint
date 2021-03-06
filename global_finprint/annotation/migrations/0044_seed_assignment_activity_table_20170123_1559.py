# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-01-23 15:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0043_create_assignment_activity_objects_20170123_1556'),
    ]

    operations = [
        migrations.RunSQL('''

        ---- update any assignment records that should be "in progress" to stat 2
        update annotation_assignment
          set status_id = 2
        where progress > 0
          and status_id = 1;

        ---- seed activity audit table
        -- initial assignment:
        INSERT INTO annotation_activity_audit
        (
          assingment_id,
          status_id,
          activity_change,
          activity_datetime
        )
        SELECT
          a.id,
          1,
          'I',
          a.create_datetime
        FROM annotation_assignment a;
        -- update assignment to whatever the current state is:
        INSERT INTO annotation_activity_audit
        (
          assingment_id,
          status_id,
          progress,
          progress_delta,
          activity_change,
          activity_datetime
        )
        select
          a.id,
          a.status_id,
          a.progress,
          a.progress,
          'U',
          a.last_modified_datetime
        from annotation_assignment a
        where a.status_id > 1;
        --------------

        '''),
    ]
