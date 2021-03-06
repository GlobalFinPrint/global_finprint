import bulk_common as bc
import openpyxl
import os
from datetime import datetime
import logging
import traceback
import collections
import click
import subprocess

ANNOTATOR = 'Conrad Speed'
ANIMAL_MAP = 'global_finprint/core/management/commands/meekan_animal_map.json'

@click.command()
@click.argument('excel_file')
@click.argument('em_files_root')
def bulk_import(excel_file, em_files_root):
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb['Set']
    get_cell = bc.get_cell_by_name_extractor(bc.get_header_map(sheet.rows[0]))
    logging.info('Looking for event measure files in "{}"'.format(em_files_root))
    for row in sheet.rows[1:]:
        trip_code = get_cell(row, 'trip_code').value
        set_code = get_cell(row, 'set_code').value
        set_date = get_cell(row, 'date').value
        if trip_code and set_code:
            video_name = get_cell(row, 'video').value
            file_to_process = None
            full_file_name = None

            logging.info('Finding event measure file for trip: {}, set: {}'.format(trip_code, set_code))
            logging.info('Video name is "{}"'.format(video_name))

            for pattern in ['{}_Dot Point Measurements.txt',
                            '{}_EV_Dot Point Measurements.txt']:
                file_to_process = pattern.format(video_name)
                full_file_name = os.path.join(em_files_root, file_to_process)
                if os.path.isfile(full_file_name):
                    logging.info('Found event measure file: "{}"'.format(file_to_process))
                    logging.info('Processing "{}"'.format(full_file_name))
                    subprocess.call(
                        'python manage.py import_event_measure {} {} "{}" --annotator="{}" --date="{}" --animal_map "{}"'.format(
                            trip_code, set_code, full_file_name, ANNOTATOR, set_date, ANIMAL_MAP),
                        shell=True
                    )
                    break
            else:
                logging.warning('No event measure files found for set "{}" of trip "{}"'.format(set_code, trip_code))

if __name__ == '__main__':
    logging.basicConfig(format='*BULK*:%(levelname)s %(asctime)s %(message)s', level=logging.INFO)
    bulk_import()
