import os
import click
import tempfile
import shutil
import subprocess
import logging
import json
import openpyxl

import bulk_common as bc

FILE_ENDING = 'mp4'

@click.command()
@click.argument('excel_file')
@click.argument('root_dir')
@click.argument('out_filename')
def get_video_lengths(excel_file, root_dir, out_filename):
    set_mapping = get_set_to_video_mapping(excel_file)
    out_file = open(out_filename, 'w')
    for root, subdirs, files in os.walk(root_dir):
        logging.info('**** Processing folder: {}'.format(root))
        mp4s = [fi for fi in files if fi.lower().endswith('.mp4') and not fi.startswith('._')]
        file_text = ''
        for vid in mp4s:
            file_path = "{}/{}".format(root, vid)
            logging.info('Grabbing details from {}'.format(file_path))

            pipe = subprocess.Popen(
                'ffprobe -v quiet -print_format json -show_format "{}"'.format(file_path),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            output = pipe.stdout.read().decode('utf-8')
            mp4_details = json.loads(output)

            try:
                duration = mp4_details['format']['duration']
                logging.info('Duration: {}'.format(duration))
                split_path = file_path.split('/')
                trip_code = ''
                set_code = ''
                folder = split_path[-2]
                video = split_path[-1]
                if folder in set_mapping:
                    trip_code, set_code = set_mapping[folder]
                out_file.write('{}\n'.format('\t'.join([trip_code, set_code, folder, video, duration])))
            except KeyError:
                logging.error('No duration returned. Bad json? Contents: {}'.format(mp4_details))
        logging.info('Finished folder.\n')

def get_set_to_video_mapping(excel_file):
    result = {}
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb['Set']
    headers = bc.get_header_map(sheet.rows[0])
    get_cell = bc.get_cell_by_name_extractor(headers)

    for idx, row in enumerate(sheet.rows[1:], start=2):
        try:
            trip_code = get_cell(row, 'trip_code').value
            set_code = get_cell(row, 'set_code').value
            video = get_cell(row, 'video').value

            result[video] = (trip_code, set_code)
        except:
            logger.error('Unable to get mapping for row %s', idx)
            logger.error(traceback.format_exc())

    return result

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
    get_video_lengths()
