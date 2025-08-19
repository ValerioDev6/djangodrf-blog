from __future__ import absolute_import, unicode_literals

import logging

from celery import shared_task

logger = logging.getLogger(__name__)
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


@shared_task
def test_task():
    logger.info("test_task")
