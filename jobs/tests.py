from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.db import transaction
from django.test.testcases import TransactionTestCase

from jobs.consumers import ProjectProgressConsumer
from project.models import Project

# Create your tests here.


class ConsumerTest(TransactionTestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('user', 'test@mail.com', 'password')
        self.project = Project.objects.create(name="Testproject")
        self.project.members.add(self.user)
        self.project.save()
        transaction.commit()

    async def test_new_connection(self):
        communicator = WebsocketCommunicator(ProjectProgressConsumer.as_asgi(), "/ws/jobs/{}/".format(self.project.id))
        communicator.scope['url_route'] = {'kwargs': {"project_id": self.project.id}}
        communicator.scope["user"] = self.user
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

    async def test_unauthorized_connection(self):
        communicator = WebsocketCommunicator(ProjectProgressConsumer.as_asgi(), "/ws/jobs/{}/".format(self.project.id))
        communicator.scope['url_route'] = {'kwargs': {"project_id": self.project.id}}
        other_user = await sync_to_async(
            lambda: get_user_model().objects.create_user('user2', 'bla@bla.com', 'password'))()
        communicator.scope["user"] = other_user
        connected, subprotocol = await communicator.connect()
        self.assertFalse(connected)
