import os
import threading
import grpc
import time
import json
import pika
from concurrent import futures
import archivos_pb2
import archivos_pb2_grpc

# Cargar la configuración desde el archivo de configuración
with open("config_mserv1.json", "r") as config_file:
    config = json.load(config_file)

# Directorio para listar archivos
directorio = config["directorio"]

# Implementación del servicio gRPC
class ListarArchivosServicer(archivos_pb2_grpc.ArchivosServicer):
    def ListarArchivos(self, request, context):
        try:
            archivos = os.listdir(directorio)
            return archivos_pb2.ListaArchivos(archivos=archivos)
        except Exception as e:
            # En caso de fallo, publicar mensaje en la cola RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='mserv1_queue')
            channel.basic_publish(exchange='', routing_key='mserv1_queue', body="Fallo en listado de archivos")
            connection.close()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error al listar archivos: ' + str(e))
            return archivos_pb2.ListaArchivos()

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    archivos_pb2_grpc.add_ArchivosServicer_to_server(ListarArchivosServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    print("Microservicio mserv1 escuchando en el puerto 50051...")

    try:
        while True:
            time.sleep(86400)  # Esperar un día antes de finalizar
    except KeyboardInterrupt:
        server.stop(0)

if _name_ == '_main_':
    main()