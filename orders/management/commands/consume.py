from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Consume orders"

    def handle(self, *args, **options):
        from ordersapi import message_queue

        message_queue.consume()
