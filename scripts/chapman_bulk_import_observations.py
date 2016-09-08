import bulk_common as bc
import os
import os.path
from datetime import datetime
import logging
import traceback
import collections
import click
import subprocess

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
    trip_code = os.path.basename(excel_files_root).split(' ')[0]
    for filename in excel_files:
        set_code = filename.split('.')[0]
        if trip_code and set_code:
            logging.info('Importing observations for trip: {}, set: {}'.format(trip_code, set_code))
        full_file_name = os.path.join(excel_files_root, filename)
        logging.info('Importing "{}"'.format(full_file_name))
        subprocess.call(
            'python manage.py import_chapman_observations {} {} "{}" "{}"'.format(
                trip_code, set_code, full_file_name, video_length_file),
            shell=True
        )

if __name__ == '__main__':
    for log_path in ['/home/ubuntu/chapman_import.log', 'chapman_import.log']:
        try:
            logging.basicConfig(
                format='%(asctime)s:%(levelname)s:%(message)s',
                level=logging.INFO,
                filename=log_path)
            break
        except FileNotFoundError:
            pass # unable to open log file
    else:
        print('Unable to open a log file!')
    bulk_import()