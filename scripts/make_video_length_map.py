import os
import click
import tempfile
import shutil
import subprocess
import logging
import json

FILE_ENDING = 'mp4'

@click.command()
@click.argument('root_dir')
@click.argument('out_filename')
def get_video_lengths(root_dir, out_filename):
    logging.info('Starting the stitching process.')
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
                out_file.write('{}\t{}\t{}\n'.format(split_path[-2], split_path[-1], duration))
            except KeyError:
                logging.error('No duration returned. Bad json? Contents: {}'.format(mp4_details))
        logging.info('Finished folder.\n')

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
    get_video_lengths()
