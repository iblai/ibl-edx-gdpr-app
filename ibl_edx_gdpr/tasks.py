from celery import task
import subprocess
from os import listdir
from os.path import isfile, join
import logging

logging.getLogger(__name__)

from ibl_edx_gdpr.config import TRACKING_LOG_PATHS
from ibl_edx_gdpr.models import RetirementBackgroundCache
from openedx.core.djangoapps.user_api.models import RetirementState, UserRetirementStatus
import logging

logging.getLogger(__name__)


@task(bind=True)
def clean_tracking_logs(self, old_value, new_value, object_id, final_task=False):
    """

    :param self:
    :param old_value: Search string
    :param new_value: Replaced with
    :param object_id: User pk
    :param final_task: When True, it means we have deleted every other record that needs to be
    deleted and we can cleanup reference models
    :return:
    """
    rbc_object = RetirementBackgroundCache.objects.create(
        old_value=old_value,
        new_value=new_value,
        is_final_task=final_task,

        object_id=object_id
    )
    logging.info("IBL_EDPR_GDPR" + f'Starting REPLACE task in directories [{TRACKING_LOG_PATHS}]')

    for path in TRACKING_LOG_PATHS:
        logging.info("IBL_EDPR_GDPR" + '*' * 15)

        logging.info("IBL_EDPR_GDPR" + f'Working in {path}')

        files = [f"{join(path, f)}" for f in listdir(path) if isfile(join(path, f))]
        files.sort()
        files.reverse()
        logging.info("IBL_EDPR_GDPR" + f"Found {files}")

        for filename in files:
            is_zipped = filename.endswith('.gz')
            if is_zipped:
                filename = filename.strip('.gz')
                # Unzip it
                logging.info("IBL_EDPR_GDPR" + f'Unzipping {filename}')
                status = subprocess.run(["gzip", "-d", filename])
                logging.info(f"IBL_EDPR_GDPR: {status}")
                logging.info(f"IBL_EDPR_GDPR: {status.stdout}")
                if status.stderr:
                    error = f"Error while unzipping, Skipping ({filename}) : {status.stderr}"
                    logging.error(error)
                    rbc_object.log_error(error)
                    continue

            logging.info("IBL_EDPR_GDPR" + f'Replacing {new_value}')
            status = subprocess.run(["sed", "-i", f"s/{old_value}/{new_value}/g", filename])

            logging.info(f"IBL_EDPR_GDPR: {status}")
            logging.info(f"IBL_EDPR_GDPR: {status.stdout}")
            if status.stderr:
                error = f"Error while replacing values for {new_value} ({filename}) : {status.stderr}"
                logging.error(error)
                rbc_object.log_error(error)
                continue

            # At this point, we have the task done
            rbc_object.set_as_completed()

            # This is a low-impact task, we ignore if it does not zip it again
            if is_zipped:
                # Return back to zip
                status = subprocess.run(["gzip", filename])
                logging.info("IBL_EDPR_GDPR" + 'Zipping Back')
                logging.info(f"IBL_EDPR_GDPR: {status}")
                logging.info(f"IBL_EDPR_GDPR: {status.stdout}")
                if status.stderr:
                    error = f"Error while zipping ({filename}) : {status.stderr}"
                    logging.error(error)
                    continue

    # Final Purge: It has checked all required files and deleted all entries
    if final_task:
        logging.info(f"IBL_EDPR_GDPR: Final task received Deleting all entries")
        UserRetirementStatus.objects.filter(user__id=object_id).update(
            original_username='', original_name='', original_email=''
        )
        # Delete it and other records
        rbc_object.delete_related_entries()


@task(bind=True)
def retirement_logs_cleanup_health_check(self):
    """
    Use this to delete completed Retirement Background Cache records
    :param self:
    :return:
    """
    FAILED_TASKS = []
    # We would group by object_ids and check if we already have completed tasks, maybe for some reason,
    # the final task fails we want to send a report of this

    related_objects = RetirementBackgroundCache.objects.values('object_id')
    for rbc_object in related_objects:
        pass
