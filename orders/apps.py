import logging
import time

import pika

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self):
        from ordersapi import message_queue

        queue_initialized = False
        while not queue_initialized:
            try:
                message_queue.initialize()
                queue_initialized = True
            except pika.exceptions.AMQPConnectionError:
                logger.warn("not connected to message queue retrying...")
                time.sleep(1)
