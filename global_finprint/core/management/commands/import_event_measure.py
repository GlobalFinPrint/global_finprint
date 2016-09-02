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
import django.db.utils as dbu

import global_finprint.core.management.commands.import_common as ic

logger = logging.getLogger('scripts')

def import_file(trip_code, set_code, filename, animal_map, annotator, date):
    logger.info('Importing trip "{}", set "{}" from file "{}"'.format(trip_code, set_code, filename))
    if animal_map:
        logger.info('Loading animal to id mappings from "{}"'.format(animal_map))
        ic.load_animal_mapping(animal_map)
    csv_file = open(filename)

    # throw away first four lines (headers are on line five)
    for _ in range(4):
        try:
            csv_file.readline()
        except UnicodeDecodeError:
            logger.error('Unable to parse binary file ("{}")'.format(filename))
            return
    obs_data = csv.DictReader(csv_file, delimiter='\t')
    import_observation_data(trip_code, set_code, obs_data, annotator=annotator, date=date)

def import_observation_data(trip_code, set_code, obs_data, annotator=None, date=None):
    for row in obs_data:
        try:
            obvs_date = string2date(date if date else row['Date'])
        except ValueError:
            logger.error('Failing import due to bad date')
            break
        except KeyError:
            logger.error('Failing due to missing Date column')
            break
        stage = None
        sex = None
        if row['Stage']:
            orig_stage_value = row['Stage']
            if orig_stage_value in ['M', 'F']:
                sex = orig_stage_value
            elif orig_stage_value == 'AD':
                stage = orig_stage_value
            elif orig_stage_value == 'J':
                stage = 'JU'
            else:
                logger.error('Unknown "Stage" value: {}'.format(orig_stage_value))
                break
        obvs_time = minutes2milliseconds(row['Time (mins)'])
        duration = None
        family = row['Family']
        genus = row['Genus']
        species = row['Species']
        behavior = row['Activity']
        length = None
        comment = row['Comment']
        if not annotator:
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
            annotation_date,
            row
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
    for format_string in ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y', '%d.%m.%y', '%d.%m.%Y']:
        try:
            result = datetime.strptime(date, format_string)
            break
        except ValueError:
            pass
    if not result:
        error_str = 'Unable to parse date: {}'.format(date)
        logger.error(error_str)
        raise ValueError(error_str)
    
    return result

class Command(BaseCommand):
    help = """Imports observation data from event measure format.
Usage: python manage.py import_event_measure <trip_code> <set_code> <in_file>"""

    def add_arguments(self, parser):
        parser.add_argument('trip_code', type=str)
        parser.add_argument('set_code', type=str)
        parser.add_argument('in_file', type=str)
        parser.add_argument('--animal_map', type=str, default=None)
        parser.add_argument('--date', type=str, default=None)
        parser.add_argument('--annotator', type=str, default=None)

    def handle(self, *args, **options):
        import_file(
            options['trip_code'],
            options['set_code'],
            options['in_file'],
            options['animal_map'],
            options['annotator'],
            options['date']
        )
