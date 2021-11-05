from typing import Dict

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Job(TimeStampedModel):
    """Base class for background jobs. Store information about ownership, progress, etc..."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_completed = self.completed_steps

    project = models.ForeignKey("project.Project", models.CASCADE)

    finished = models.DateTimeField(null=True, blank=True)

    total_steps = models.PositiveIntegerField()
    completed_steps = models.PositiveIntegerField(default=0)

    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.__old_completed != self.completed_steps:
            print("Sending update...")
            send_update(self, {'steps': self.completed_steps})

        super().save(*args, **kwargs)
        self.__old_completed = self.completed_steps

    def __str__(self):
        return self.name


class Result(TimeStampedModel):
    """Basic information about a result."""
    message = models.CharField(max_length=255)
    needs_intervention = models.BooleanField(default=False)
    job = models.ForeignKey(Job, models.CASCADE)
    state = models.IntegerField()

    def save(self, *args, **kwargs):
        is_new = False

        if self.pk is None:
            is_new = True

        super().save(*args, **kwargs)

        if is_new:
            send_finished(self.job)

    def __str__(self):
        return self.result


class LogMessage(TimeStampedModel):
    """A message associated with a job."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3

    LOG_LEVELS = (
        (DEBUG, _("debug")),
        (INFO, _("info")),
        (WARNING, _("warning")),
        (ERROR, _("error")),
    )

    job = models.ForeignKey(Job, models.CASCADE)
    message = models.CharField(max_length=500)
    level = models.IntegerField(default=0, choices=LOG_LEVELS)

    def save(self, *args, **kwargs):
        is_new = False

        if self.pk is None:
            is_new = True

        super().save(*args, **kwargs)

        if is_new:
            send_update(self.job, {'log': self.message})

    def __str__(self):
        return self.message


def send_update(job, message: Dict):
    channel_layer = get_channel_layer()
    message['project_id'] = job.project.id.hex
    message['type'] = 'jobs.update'

    async_to_sync(channel_layer.group_send)("jobs", message)


def send_finished(job):
    channel_layer = get_channel_layer()
    message = {
        'project_id': job.project.id.hex,
        'type': 'jobs.finished',
        'job': job.id,
    }

    result = Result.objects.filter(job=job).first()

    if result is not None:
        message['result'] = {
            'message': result.message,
            'needs_intervention': result.needs_intervention,
            'state': result.state,
        }

    async_to_sync(channel_layer.group_send)("jobs", message)
