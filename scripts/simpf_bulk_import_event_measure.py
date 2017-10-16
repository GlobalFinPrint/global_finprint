import bulk_common as bc
import openpyxl
import os
from datetime import datetime
import logging
import traceback
import collections
import click
import subprocess
import re

ANIMAL_MAP = 'global_finprint/core/management/commands/sherman_animal_map.json'

@click.command()
@click.argument('excel_file')
@click.argument('em_files_root')
def bulk_import(excel_file, em_files_root):
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb['Set']
    get_cell = bc.get_cell_by_name_extractor(bc.get_header_map(sheet[1]))
    for row in sheet.iter_rows(row_offset=1):
        trip_code = get_cell(row, 'trip_code').value
        set_code = get_cell(row, 'set_code').value
        if trip_code and set_code:
            logging.info('Finding event measure folder for trip: {}, set: {}'.format(trip_code, set_code))
        em_folder_name = get_cell(row, 'video').value
        parent_folder = re.match('[^\d_]+', em_folder_name)
        if not parent_folder:
            logging.error('Problem parsing folder name')
            break
        em_path = os.path.join(em_files_root, trip_code, parent_folder.group(), em_folder_name)
        logging.info('Checking folder "{}"'.format(em_path))
        try:
            txt_files = [fi for fi in os.listdir(em_path) if fi.lower().endswith('.txt') and not fi.startswith('.')]
        except:
            logging.warn('No event measure files found for set "{}" of trip "{}"'.format(set_code, trip_code))
            continue
        files_by_annotator = collections.defaultdict(list)
        for a_file in txt_files:
            pieces = a_file[:-4].split('_')
            if len(pieces) >= 4:
                annotator = pieces[3]
                if annotator in ['MaxN',
                                 'PointMeasurements',
                                 ' Point Measurements',
                                 'Dot Point Measurements',
                                 'Point Measurements']:
                    annotator = pieces[-1]
                files_by_annotator[annotator].append(a_file)
        logging.info('All candidate files: {}'.format(txt_files))
        for annotator in files_by_annotator:
            file_to_process = ''
            candidates = files_by_annotator[annotator]
            for file_contents in ['edit_pullperiod_dot point measurements',
                                  'pullperiod_dot point measurements',
                                  'edit_dot point measurements',
                                  'dot point measurements',
                                  'dotpointmeasurements',
                                  'pointmeasurements',
                                  'point measurements',
                                  'dotpoint',
                                  'point_measurements']:
                tmp_candidates = [xx for xx in candidates if xx.lower().find(file_contents) >= 0]
                if len(tmp_candidates) > 0:
                    tmp_candidates.sort(key=lambda x: os.stat(os.path.join(em_path, x)).st_mtime, reverse=True)
                    file_to_process = tmp_candidates[0]
                    break
            if file_to_process:
                full_file_name = os.path.join(em_path, file_to_process)
                logging.info('Processing "{}"'.format(os.path.join(em_path, file_to_process)))
                subprocess.call(
                    'python manage.py import_event_measure {} {} "{}" --animal_map "{}"'.format(trip_code, set_code, full_file_name, ANIMAL_MAP),
                    shell=True
                )

            else:
                logging.error('Unable to find file for annotator "{}" in folder "{}"'.format(annotator, em_path))

if __name__ == '__main__':
    logging.basicConfig(format='*BULK*:%(levelname)s %(asctime)s %(message)s', level=logging.INFO)
    bulk_import()

