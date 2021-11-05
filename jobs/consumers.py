from uuid import UUID

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.core.exceptions import PermissionDenied

from project.models import Project


class ProjectProgressConsumer(JsonWebsocketConsumer):
    """Listens to progress of jobs of a project and informs users about progress."""
    def connect(self):
        self.user = self.scope['user']
        self.project_id = self.scope['url_route']['kwargs']['project_id']

        if not Project.objects.filter(id=self.project_id, members=self.user):
            self.close()
            return

        async_to_sync(self.channel_layer.group_add)("jobs", self.channel_name)
        self.accept()

    def jobs_update(self, update):
        if update['project_id'] == self.project_id.hex:
            self.send_json(update)


class JobFinishedConsumer(JsonWebsocketConsumer):
    """Listen for finished jobs, and send all jobs that the user has access to."""
    def connect(self):
        self.user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)("jobs", self.channel_name)
        self.accept()

    def jobs_finished(self, message):
        if Project.objects.filter(id=message['project_id'], members=self.user).exists():
            self.send_json(message)
