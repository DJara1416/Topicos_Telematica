# https://medium.com/better-programming/introduction-to-message-queue-with-rabbitmq-python-639e397cb668
# consumer.py
# Consume RabbitMQ queue

import json
import pika
import glob
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
RMQ_HOST = os.getenv('RMQ_HOST')
RMQ_PORT = os.getenv('RMQ_PORT')
RMQ_USER = os.getenv('RMQ_USER')
RMQ_PASS = os.getenv('RMQ_PASS')

dir = "./../assets"

connection = pika.BlockingConnection(pika.ConnectionParameters(RMQ_HOST, RMQ_PORT, '/', pika.PlainCredentials(RMQ_USER, RMQ_PASS)))
channel = connection.channel()

def list_files(ch, method, properties, body):
    response = []

    for file_name in os.listdir(dir):
        file_info = {}
        file_info["name"] = file_name
        file_path = os.path.join(dir, file_name)

        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            time = os.path.getmtime(file_path)
            timestamp = datetime.datetime.fromtimestamp(time)
            formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            file_info["size"] = size
            file_info["timestamp"] = formatted_date

            response.append(file_info)

    print(f'The response in LIST is : {response}')
    publish_response(ch, method, properties, response)

def find_files(ch, method, properties, body):
    response = []

    search = body.decode('utf-8')
    for filename in glob.glob(f"{dir}/{search}"):
        file_info = {}
        file_info["name"] = os.path.basename(filename)
        size = os.path.getsize(filename)
        time = os.path.getmtime(filename)
        timestamp = datetime.datetime.fromtimestamp(time)
        formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
        file_info["size"] = size
        file_info["timestamp"] = formatted_date

        response.append(file_info)

    print(f'The response in FIND is : {response}')
    publish_response(ch, method, properties, response)

def publish_response(ch, method, properties, response):
    print("properties:", properties)
    print("Reply_to:", properties.reply_to)
    print("Corr_id:", properties.correlation_id)

    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id,
        ),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Response sent to RabbitMQ!")
    
channel.basic_consume(queue="list_queue", on_message_callback=list_files, auto_ack=False)
channel.basic_consume(queue="find_queue", on_message_callback=find_files, auto_ack=False)
channel.start_consuming()