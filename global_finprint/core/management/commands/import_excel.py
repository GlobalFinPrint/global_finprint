"""
import_excel
Author: Tyler Sellon

Adds "import_excel" command, accessible through manage.py.

Takes a single excel workbook and imports the data.

File format is specified here:
https://www.dropbox.com/s/5yy0bb4mxbm0mdj/data_collection_standards.xlsx?dl=0
"""
import openpyxl
import os
import logging
import traceback

from django.core.management.base import BaseCommand, CommandError

import global_finprint.core.management.commands.import_common as ic
import global_finprint.core.management.commands.excel_common as ec

logger = logging.getLogger('scripts')

def import_file(in_file):
    wb = ec.open_workbook(in_file)

    import_trip_data(wb['Trip'])
    import_set_data(wb['Set'])
    import_environment_data(wb['Environment'])
    import_observation_data(wb['Observation'])

def import_trip_data(sheet):
    headers = ec.get_header_map(sheet.rows[0])
    get_cell = ec.get_cell_by_name_extractor(headers)
    for idx, row in enumerate(sheet.rows[1:], start=2):
        try:
            trip_code = get_cell(row, 'code').value
            if trip_code:
                location_name = get_cell(row, 'location').value
                start_date = ec.get_date_from_cell(get_cell(row, 'start_date'))
                end_date = ec.get_date_from_cell(get_cell(row, 'end_date'))
                investigator = get_cell(row, 'investigator').value
                collaborator = get_cell(row, 'collaborator').value
                boat = get_cell(row, 'boat').value

                ic.import_trip(
                    trip_code,
                    location_name,
                    start_date,
                    end_date,
                    investigator,
                    collaborator,
                    boat
                )
        except:
            logger.error('Unable to import trip data for row %s', idx)
            logger.error(traceback.format_exc())

def import_set_data(sheet):
    headers = ec.get_header_map(sheet.rows[0])
    get_cell = ec.get_cell_by_name_extractor(headers)
    for idx, row in enumerate(sheet.rows[1:], start=2):
        try:
            set_code = get_cell(row, 'set_code').value
            if set_code:
                trip_code = get_cell(row, 'trip_code').value
                set_date = ec.get_date_from_cell(get_cell(row, 'date'))
                latitude = get_cell(row, 'latitude').value
                longitude = get_cell(row, 'longitude').value
                try:
                    depth_cell = get_cell(row, 'depth')
                    depth = ec.get_float_from_cell(depth_cell)
                except ValueError:
                    logger.error('Bad depth value "%s"', depth_cell.value)
                    logger.error('Set "%s" not created', set_code)
                    continue
                drop_time = ec.get_time_from_cell(get_cell(row, 'drop_time'), format_str='%H:%M')
                haul_time = ec.get_time_from_cell(get_cell(row, 'haul_time'), format_str='%H:%M')
                site_name = ec.get_cell_value(get_cell(row, 'site'))
                reef_name = ec.get_cell_value(get_cell(row, 'reef'))
                habitat_type = get_cell(row, 'habitat').value
                equipment_str = get_cell(row, 'equipment').value
                bait_str = get_cell(row, 'bait').value
                visibility = get_cell(row, 'visibility').value
                video = get_cell(row, 'video').value
                video_name_array = [trip_code, set_code]
                video_format = 'mp4'
                try:
                    video_format_tmp = get_cell(row, 'FORMAT').value.lower()
                    if video_format_tmp:
                        video_format = video_format_tmp
                except KeyError:
                    pass # column not included in this spreadsheet
                try:
                    camera = get_cell(row, 'camera').value
                    if camera:
                        video_name_array.append(camera)
                except KeyError:
                    pass # No camera column
                video_name = '{}.{}'.format('_'.join(video_name_array), video_format)
                logger.info('Video name: {}'.format(video_name))
                comment = get_cell(row, 'comment').value

                ic.import_set(
                    set_code,
                    trip_code,
                    set_date,
                    latitude,
                    longitude,
                    depth,
                    drop_time,
                    haul_time,
                    site_name,
                    reef_name,
                    habitat_type,
                    equipment_str,
                    bait_str,
                    visibility,
                    video,
                    video_name,
                    comment
                )                
        except:
            logger.error('Unable to import set data for row %s', idx)
            logger.error(traceback.format_exc())
            

def import_environment_data(sheet):
    headers = ec.get_header_map(sheet.rows[0])
    get_cell = ec.get_cell_by_name_extractor(headers)
    for idx, row in enumerate(sheet.rows[1:], start=2):
        try:
            trip_code = get_cell(row, 'trip_code').value
            if trip_code:
                set_code = get_cell(row, 'set_code').value
                reading_date = ec.get_date_from_cell(get_cell(row, 'date'))
                drop_haul = get_cell(row, 'drop_haul').value
                temp = ec.get_float_from_cell(get_cell(row, 'temp'))
                salinity = ec.get_float_from_cell(get_cell(row, 'salinity'))
                conductivity = ec.get_float_from_cell(get_cell(row, 'conductivity'))
                dissolved_oxygen = ec.get_float_from_cell(get_cell(row, 'dissolved_oxygen'))
                current_flow = None #get_float_from_cell(get_cell(row, 'current_flow'))
                current_direction = get_cell(row, 'current_direction').value
                tide_state = ec.get_cell_value(get_cell(row, 'tide_state'))
                wind_speed = ec.get_float_from_cell(get_cell(row, 'wind_speed'))
                wind_direction = get_cell(row, 'wind_direction').value
                cloud_cover = ec.get_float_from_cell(get_cell(row, 'cloud_cover'))
                surface_chop = get_cell(row, 'surface_chop').value

                ic.import_environment_measure(
                    trip_code,
                    set_code,
                    reading_date,
                    drop_haul.lower() == 'drop',
                    temp,
                    salinity,
                    conductivity,
                    dissolved_oxygen,
                    current_flow,
                    current_direction,
                    tide_state,
                    wind_speed,
                    wind_direction,
                    cloud_cover,
                    surface_chop
                )
        except:
            logger.error('Unable to import environment data for row %s', idx)
            logger.error(traceback.format_exc())


def import_observation_data(sheet):
    headers = ec.get_header_map(sheet.rows[0])
    get_cell = ec.get_cell_by_name_extractor(headers)
    for row in sheet.rows[1:]:
        trip_code = get_cell(row, 'trip_code').value
        if trip_code:
            set_code = get_cell(row, 'set_code').value
            obvs_date = ec.get_date_from_cell(get_cell(row, 'date'))
            obvs_time = get_cell(row, 'time').value
            duration = get_cell(row, 'duration').value
            family = get_cell(row, 'family').value
            genus = get_cell(row, 'genus').value
            species = get_cell(row, 'species').value
            behavior = get_cell(row, 'behaviour').value
            sex = get_cell(row, 'sex').value
            stage = get_cell(row, 'stage').value
            length = get_cell(row, 'length').value
            comment = get_cell(row, 'comment').value
            annotator = get_cell(row, 'annotator').value
            annotation_date = ec.get_date_from_cell(get_cell(row, 'date'))

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
                None
            )

class Command(BaseCommand):
    help = 'Imports observation data from excel format. Usage: python manage.py import_excel <excel_file>'

    def add_arguments(self, parser):
        parser.add_argument('in_file', type=str)

    def handle(self, *args, **options):
        import_file(options['in_file'])
