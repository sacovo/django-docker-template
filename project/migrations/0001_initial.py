# Generated by Django 3.2.9 on 2021-11-05 11:07

import uuid

import django.utils.timezone
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('created',
                 model_utils.fields.AutoCreatedField(default=django.utils.timezone.now,
                                                     editable=False,
                                                     verbose_name='created')),
                ('modified',
                 model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now,
                                                          editable=False,
                                                          verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]