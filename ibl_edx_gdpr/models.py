from django.db import models
import logging
logging.getLogger(__name__)

class RetirementBackgroundCache(models.Model):
    old_value = models.Charfield(max_length=255, default='')
    new_value = models.Charfield(max_length=255, default='')
    is_final_task = models.BoolenField(default=False)
    completed = models.BoolenField(default=False)

    object_id = models.Charfield(max_length=127, default='')
    error = models.TextField(default='')
    last_updated = models.DatetimeField(auto_now=True)

    def log_error(self, message):
        self.error = message
        self.save()

    def set_as_completed(self):
        self.completed = True
        self.save()

    def delete_related_entries(self, name=__name__):
        logging.getLogger(name)
        # Removing completed tasks only, We can look at tasks that have not completed and attempt to fix later on
        objects = RetirementBackgroundCache.objects.filter(object_id=self.object_id, completed=True)
        logging.info(f"Found {objects.count()} related completed objects. Deleting...")
        objects.delete()
        logging.info('Deleted')
