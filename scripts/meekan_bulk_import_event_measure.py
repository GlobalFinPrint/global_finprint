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

@click.command()
@click.argument('excel_file')
@click.argument('em_files_root')
def bulk_import(excel_file, em_files_root):
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb['Set']
    get_cell = bc.get_cell_by_name_extractor(bc.get_header_map(sheet.rows[0]))
    for row in sheet.rows[1:]:
        trip_code = get_cell(row, 'trip_code').value
        set_code = get_cell(row, 'set_code').value
        set_date = get_cell(row, 'date').value
        if trip_code and set_code:
            logging.info('Finding event measure folder for trip: {}, set: {}'.format(trip_code, set_code))
        video_name = get_cell(row, 'video').value
        try:
            txt_files = [fi for fi in os.listdir(em_files_root)
                         if fi.lower().endswith('.txt') and not fi.startswith(video_name)]
        except:
            logging.warn('No event measure files found for set "{}" of trip "{}"'.format(set_code, trip_code))
            continue
        if len(txt_files) < 1:
            logging.error('No event measure files found for set "{}" of trip "{}"'.format(set_code, trip_code))
            break
        else:
            file_to_process = txt_files[0] # TODO: pick this correctly
            full_file_name = os.path.join(em_files_root, file_to_process)
            logging.info('Processing "{}"'.format(os.path.join(em_files_root, file_to_process)))
            subprocess.call(
                'python manage.py import_event_measure {} {} "{}" --annotator="{}" --date="{}"'.format(trip_code, set_code, full_file_name, ANNOTATOR, set_date),
                shell=True
            )

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.WARN, filename='/home/ubuntu/meekan_import.log')
    bulk_import()
