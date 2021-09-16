from celery import task
import subprocess
from os import listdir
from os.path import isfile, join
import logging
logging.getLogger(__name__)

from ibl_edx_gdpr.config import TRACKING_LOG_PATH


@task()
def clean_tracking_logs(mapping):
    old = mapping.get('old', None)
    new = mapping.get('new', None)

    for path in TRACKING_LOG_PATH:
        files = [f for f in listdir(path) if isfile(join(path, f))]
        files.sort()
        files.reverse()
        for filename in files:
            is_zipped = filename.endswith('.gz')
            if is_zipped:
                # Unzip it
                status = subprocess.run(["gzip", "-d", filename])
                if status.stderr:
                    logging.error(f"Error while unzipping, Skipping ({filename}) : {status.stderr}")
                    continue

            status = subprocess.run(["sed", "-i", f"s/{old}/{new}/g", filename])
            if status.stderr:
                logging.error(f"Error while replacing values for {new} ({filename}) : {status.stderr}")

            if is_zipped:
                # Return back to zip
                filename = filename.strip('.gz')
                status = subprocess.run(["gzip", filename])
                if status.stderr:
                    logging.error(f"Error while zipping ({filename}) : {status.stderr}")
