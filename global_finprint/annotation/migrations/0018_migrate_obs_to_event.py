from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0017_auto_20160516_0030'),
    ]

    operations = [
        migrations.RunSQL('''
        -- migrate initial observations to an event
        insert into annotation_event
            (
              create_datetime,
              last_modified_datetime,
              observation_id,
              event_time,
              extent,
              note,
              user_id
            )
            select distinct
              create_datetime,
              last_modified_datetime,
              id,
              initial_observation_time,
              extent,
              comment,
              user_id
            from annotation_observation;

        -- migrate behaviors to event attributes
        --INSERT INTO annotation_eventattribute () select ...;

        --migrate gear to event attributes
        --INSERT INTO annotation_eventattribute () select ...;

        --migrate gear to event attributes
        --INSERT INTO annotation_eventattribute () select ...;

        '''),
    ]
