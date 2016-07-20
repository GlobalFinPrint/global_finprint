from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bruv', '0008_auto_20160719_1751'),
    ]

    operations = [
        migrations.RunSQL('''
            --- WHOOPS!
            UPDATE bruv_bait
            SET description = 'Pilchards'
            WHERE description = 'Pilcahrds';
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
