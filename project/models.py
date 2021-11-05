import uuid

from django.contrib.auth import get_user_model
from django.db import models
from model_utils.models import TimeStampedModel


class Project(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    name = models.CharField(max_length=255)
    members = models.ManyToManyField(get_user_model())

    def __str__(self):
        return self.name
