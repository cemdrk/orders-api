import os

import pika

RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]

EXCHANGE_NAME = os.environ["EXCHANGE_NAME"]
QUEUE_NAME = os.environ["QUEUE_NAME"]


def initialize():
    connection_parameters = pika.ConnectionParameters(RABBITMQ_HOST)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.exchange_declare(EXCHANGE_NAME)
    channel.queue_declare(queue=QUEUE_NAME)
    channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME)
    channel.close()


def publish(message):
    connection_parameters = pika.ConnectionParameters(RABBITMQ_HOST)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.basic_publish(
        exchange=EXCHANGE_NAME, routing_key=QUEUE_NAME, body=str(message)
    )
    channel.close()


def on_message(channel, method_frame, header_frame, body):
    from orders.models import Order

    order = Order.objects.get(id=int(body))
    order.accept()
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def consume():
    connection_parameters = pika.ConnectionParameters(RABBITMQ_HOST)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
    channel.start_consuming()
