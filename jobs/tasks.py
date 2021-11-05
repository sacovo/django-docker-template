from typing import Dict

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from jobs.models import Result


def send_update(job, message: Dict):
    channel_layer = get_channel_layer()

    message['project_id'] = job.project.id
    message['type'] = 'jobs.update'

    async_to_sync(channel_layer.group_send)("jobs", message)


def send_finished(job):
    channel_layer = get_channel_layer()
    message = {
        'project_id': job.project.id,
        'type': 'jobs.finished',
        'job': job.id,
    }

    result = Result.objects.filter(job=job).first()

    if result is not None:
        message['result'] = {
            'message': result.message,
            'needs_intervention': result.needs_intervention,
            'state': result.sate,
        }

    async_to_sync(channel_layer.group_send)("jobs", message)
