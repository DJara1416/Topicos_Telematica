# https://medium.com/better-programming/introduction-to-message-queue-with-rabbitmq-python-639e397cb668
# consumer.py
# Consume RabbitMQ queue

import pika
import os
from dotenv import load_dotenv

load_dotenv()

IP_ELASTICA_RABBITMQ = os.getenv('44.195.244.252')
USUARIO_RABBITMQ = os.getenv('user')
PASSWORD_RABBITMQ = os.getenv('password')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("user", "password")))
channel = connection.channel()

def callback(ch, method, properties, body):
    print(f'{body} is received')
    
channel.basic_consume(queue="my_app", on_message_callback=callback, auto_ack=True)
channel.start_consuming()