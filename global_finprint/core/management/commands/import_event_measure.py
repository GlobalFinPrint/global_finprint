"""
import_event_measure
Author: Tyler Sellon

Adds "import_event_measure" command, accessible through manage.py.

Takes a single event measure csv and imports the data.
"""
import os
from datetime import datetime
import logging
import csv
import json

from django.core.management.base import BaseCommand, CommandError

import global_finprint.core.management.commands.import_common as ic

logger = logging.getLogger('scripts')

def import_file(trip_code, set_code, filename):
    logger.info('Importing trip "{}", set "{}" from file "{}"'.format(trip_code, set_code, filename))
    csv_file = open(filename)

    # throw away first four lines (headers are on line five)
    for _ in range(4):
        try:
            csv_file.readline()
        except UnicodeDecodeError:
            logger.error('Unable to parse binary file ("{}")'.format(filename))
            return
    obs_data = csv.DictReader(csv_file, delimiter='\t')
    import_observation_data(trip_code, set_code, obs_data)

def import_observation_data(trip_code, set_code, obs_data):
    is_set_data_imported = False
    for row in obs_data:
        if not is_set_data_imported:
            try:
                ic.update_set_data(trip_code, set_code, row['Visibility'])
            except KeyError:
                logger.error('Data is missing column "Visibility"')
                continue
        obvs_date = string2date(row['Date'])
        obvs_time = minutes2milliseconds(row['Time (mins)'])
        duration = minutes2milliseconds(row['Period time (mins)'])
        family = row['Family']
        genus = row['Genus']
        species = row['Species']
        behavior = row['Activity']
        sex = row['Stage']
        stage = None
        length = None
        comment = json_args = json.dumps(row, sort_keys=True, default=lambda a: a.isoformat())
        try:
            annotator = row['TapeReader']
        except KeyError:
            annotator = row['Tape Reader']
        annotation_date = None

        ic.import_observation(
            trip_code,
            set_code,
            obvs_date,
            obvs_time,
            duration,
            family,
            genus,
            species,
            behavior,
            sex,
            stage,
            length,
            comment,
            annotator,
            annotation_date
        )

def minutes2milliseconds(minutes):
    """
    Converts minutes to milliseconds.
    :param minutes: duration in minutes as string
    :return: duration in milliseconds as int
    """
    if minutes:
        return round(float(minutes) * 60 * 1000)
    else:
        return 0

def string2date(date):
    """
    Parses a date string.
    :param date: date in a string format
    :return: date as datetime
    """
    result = None
    for format_string in ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d.%m.%y', '%d.%m.%Y']:
        try:
            result = datetime.strptime(date, format_string)
            break
        except ValueError:
            pass
    if not result:
        raise ValueError('Unable to parse date: {}'.format(date))
    
    return result

class Command(BaseCommand):
    help = """Imports observation data from event measure format.
Usage: python manage.py import_event_measure <trip_code> <set_code> <in_file>"""

    def add_arguments(self, parser):
        parser.add_argument('trip_code', type=str)
        parser.add_argument('set_code', type=str)
        parser.add_argument('in_file', type=str)

    def handle(self, *args, **options):
        import_file(
            options['trip_code'],
            options['set_code'],
            options['in_file']
        )
