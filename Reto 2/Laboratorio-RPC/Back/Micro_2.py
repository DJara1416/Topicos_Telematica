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
with open("config_mserv2.json", "r") as config_file:
    config = json.load(config_file)

# Directorio para buscar archivos
directorio = config["directorio"]

# Implementación del servicio gRPC
class BuscarArchivosServicer(archivos_pb2_grpc.ArchivosServicer):
    def BuscarArchivos(self, request, context):
        try:
            patron = request.patron
            archivos_encontrados = [archivo for archivo in os.listdir(directorio) if patron in archivo]
            return archivos_pb2.ListaArchivos(archivos=archivos_encontrados)
        except Exception as e:
            # En caso de fallo, publicar mensaje en la cola RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='mserv2_queue')
            channel.basic_publish(exchange='', routing_key='mserv2_queue', body="Fallo en búsqueda de archivos")
            connection.close()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Error al buscar archivos: ' + str(e))
            return archivos_pb2.ListaArchivos()

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    archivos_pb2_grpc.add_ArchivosServicer_to_server(BuscarArchivosServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()

    print("Microservicio mserv2 escuchando en el puerto 50052...")

    try:
        while True:
            time.sleep(86400)  # Esperar un día antes de finalizar
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    main()