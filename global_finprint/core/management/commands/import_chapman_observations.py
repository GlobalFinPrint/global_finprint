"""
import_chapman_observations
Author: Tyler Sellon

Adds "import_chapman_observations" command, accessible through manage.py.

The Chapman-Valentin team has their own excel format for observation data.
This command takes a single excel workbook in that format and imports the data.

File format is specified here:
https://www.dropbox.com/s/5yy0bb4mxbm0mdj/data_collection_standards.xlsx?dl=0
"""
import os
import logging
import traceback
import json
import csv

from django.core.management.base import BaseCommand, CommandError

import global_finprint.core.management.commands.import_common as ic
import global_finprint.core.management.commands.excel_common as ec

logger = logging.getLogger('scripts')
video_length_map = None

def import_file(in_file, trip_code, set_code, video_length_file):
    global video_length_map
    video_length_map = get_video_length_map(video_length_file)

    logging.info('Importing observations from file "{}"'.format(in_file))
    wb = ec.open_workbook(in_file)

    for last_name in wb.sheetnames:
        import_observation_data(wb[last_name], trip_code, set_code, last_name)

def import_observation_data(sheet, trip_code, set_code, last_name):
    try:
        obsv_date, set_dict = get_set_level_fields(sheet)
    except:
        logger.error('Failed to parse set level data')
        logger.error(traceback.format_exc())
        return

    logging.info('Importing observations for annotator "{}"'.format(last_name))

    headers = ec.get_header_map(sheet.rows[3])
    get_cell = ec.get_cell_by_name_extractor(headers)
    cur_video = None
    cur_offset = 0
    next_offset = 0
    try:
        set_videos_map = video_length_map[trip_code][set_code]
    except KeyError:
        logger.error('Unable to find video info for trip "{}", set "{}".'.format(trip_code, set_code))
        return
    for idx, row in enumerate(sheet.rows[4:], start=5):
        try:
            basename = ec.get_cell_value(get_cell(row, 'File'))
            if not basename in [None, '']:
                if basename.lower().endswith('.mp4'):
                    filename = basename
                else:
                    filename = '{}.MP4'.format(basename).lower()
                if cur_video != filename:
                    if filename in set_videos_map:
                        cur_video = filename
                        cur_offset = next_offset
                        next_offset += set_videos_map[filename]
                        logger.info('Switching to video "{}", offset is now "{}"'.format(filename, cur_offset))
                    else:
                        logger.error('Video length for "{}" not found in mapping file.'.format(filename))
                        break
            obsv_time = ic.time2milliseconds(ec.get_time_from_cell(get_cell(row, 'Timestamp'))) + cur_offset
            duration = None
            family = None
            genus = ec.get_cell_value(get_cell(row, 'Genus'))
            species = ec.get_cell_value(get_cell(row, 'Species'))
            behavior = None
            sex = None
            stage = None
            length = None
            comment_pieces = []
            for column_pieces in ['Notes', 'Comments']:
                try:
                    piece = get_cell(row, 'Notes').value
                    if piece:
                        comment_pieces.append(piece)
                except KeyError:
                    pass # Column not found
            comment = '\n'.join(comment_pieces)
            annotator = last_name
            annotation_date = None
            raw_import_json = {
                'set': set_dict,
                'row': get_dict_from_row(headers, row, get_cell),
                'row_number': idx
            }

            ic.import_observation(
                trip_code,
                set_code,
                obsv_date,
                obsv_time,
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
                raw_import_json
            )
        except:
            logger.error('Unable to import observation data for row %s', idx)
            logger.error(traceback.format_exc())

def get_set_level_fields(sheet):
    headers = ec.get_header_map(sheet.rows[0])
    get_cell = ec.get_cell_by_name_extractor(headers)
    row = sheet.rows[1]
    obsv_date = ec.get_date_from_cell(get_cell(row, 'Date'))

    return obsv_date, get_dict_from_row(headers, row, get_cell)

def get_dict_from_row(headers, row, get_cell_func):
    result = {}
    for key in headers:
        result[key] = str(get_cell_func(row, key).value)
    return result

def get_video_length_map(video_length_file):
    result = {}
    vlf = csv.reader(open(video_length_file), delimiter='\t')
    for row in vlf:
        trip_code = row[0]
        set_code = row[1]
        folder = row[2]
        video = row[3].lower()
        length_ms = round(float(row[4]) * 1000)

        if trip_code not in result:
            result[trip_code] = {}
        trip_dict = result[trip_code]
        if set_code not in trip_dict:
            trip_dict[set_code] = {}
        set_dict = trip_dict[set_code]
        set_dict[video] = length_ms
    return result

class Command(BaseCommand):
    help = 'Imports observation data from excel format. Usage: python manage.py import_chapman_observations <excel_file>'

    def add_arguments(self, parser):
        parser.add_argument('trip_code', type=str)
        parser.add_argument('set_code', type=str)
        parser.add_argument('in_file', type=str)
        parser.add_argument('video_length_map', type=str)

    def handle(self, *args, **options):
        import_file(options['in_file'], options['trip_code'], options['set_code'], options['video_length_map'])
