from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bruv', '0008_auto_20160719_1751'),
    ]

    operations = [
        migrations.RunSQL('''
        with good_bait as (
            select id from bruv_bait WHERE description = 'Pilchards' AND type = 'CRS' AND oiled = FALSE LIMIT 1
        ),
        bad_bait as (
            select id from bruv_bait WHERE description = 'Pilcahrds' AND type = 'CRS' AND oiled = FALSE LIMIT 1
        ),
        bad_rows AS (
            select id from bruv_set WHERE bait_id in (select id from bad_bait)
        )
        update bruv_set set bait_id = good_bait.id from good_bait where bait_id in (select id from bad_bait);
    '''),
        migrations.RunSQL('''
            --- pick first instance of dupe
            WITH baits AS
            (
                SELECT DISTINCT
                  min(id) AS id,
                  description,
                  type,
                  oiled,
                  25      AS user_id
                FROM bruv_bait
                GROUP BY
                  description,
                  type,
                  oiled
            )
            UPDATE bruv_set
            SET bait_id = baits.id
            FROM bruv_bait b,
              baits
            WHERE
              bruv_set.bait_id = b.id
              AND b.description = baits.description
              AND b.type = baits.type;
          '''),
        migrations.RunSQL('''
            --- clean up unused
            DELETE FROM bruv_bait
            WHERE bruv_bait.id NOT IN
                  (
                    SELECT bait_id
                    FROM bruv_set
                  );
        '''),
    ]
