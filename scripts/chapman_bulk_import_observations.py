import bulk_common as bc
import os
import os.path
from datetime import datetime
import logging
import traceback
import collections
import click
import subprocess

ANIMAL_MAP = 'global_finprint/core/management/commands/chapman_animal_map.json'

@click.command()
@click.argument('excel_files_root')
@click.argument('video_length_file')
def bulk_import(excel_files_root, video_length_file):
    logging.info('Starting import process for files in "{}"'.format(excel_files_root))
    try:
        excel_files = [fi for fi in os.listdir(excel_files_root)
                       if fi.lower().endswith('.xlsx')]
    except:
        logging.warn('No excel files found in "{}"'.format(excel_files_root))
    if excel_files_root[-1] == '/':
        excel_files_root = excel_files_root[:-1]
    trip_code = os.path.basename(excel_files_root).split(' ')[0]
    for filename in excel_files:
        set_code = filename.split('.')[0]
        if trip_code and set_code:
            logging.info('Importing observations for trip: {}, set: {}'.format(trip_code, set_code))
        full_file_name = os.path.join(excel_files_root, filename)
        logging.info('Importing "{}"'.format(full_file_name))
        command_str = 'python manage.py import_chapman_observations {} {} "{}" "{}" --animal_map "{}"'.format(
            trip_code, set_code, full_file_name, video_length_file, ANIMAL_MAP)
        logging.info('Running command: {}'.format(command_str))
        subprocess.call(
            command_str,
            shell=True
        )

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        level=logging.INFO)
    bulk_import()
