from django.db import connection

REPORT_PREFIX = 'v_report_'


class Report:
    def __init__(self, db_view):
        self.db_view = db_view if REPORT_PREFIX in db_view else '{}{}'.format(REPORT_PREFIX, db_view)

    @classmethod
    def view_list(cls):
        with connection.cursor() as cursor:
            query = "SELECT table_name FROM INFORMATION_SCHEMA.views " \
                    "WHERE table_name LIKE '{}%%'".format(REPORT_PREFIX)
            cursor.execute(query)
            return list(cls(row[0]) for row in cursor.fetchall())

    def results(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM {}".format(self.db_view))
            return [tuple(col[0] for col in cursor.description)] + cursor.fetchall()

    def __str__(self):
        return u'{}'.format(self.db_view.replace(REPORT_PREFIX, ''))
