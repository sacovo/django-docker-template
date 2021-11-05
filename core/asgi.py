"""
ASGI config for {{ project_name }} project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls.conf import path

from jobs.consumers import JobFinishedConsumer, ProjectProgressConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    "http":
    get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)
    "websocket":
    AuthMiddlewareStack(
        URLRouter([
            path("ws/jobs/results/", JobFinishedConsumer.as_asgi()),
            path("ws/jobs/<uuid:project_id>/", ProjectProgressConsumer.as_asgi()),
        ]))
})
