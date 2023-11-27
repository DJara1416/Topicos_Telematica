######## SOLO IMPRIME LOS MENSAJES RECIBIDOS  DE KAFKA########

from confluent_kafka import Consumer, KafkaException, KafkaError
import sys
import json

def create_consumer(config, topic):
    # Crear el consumidor de Kafka
    consumer = Consumer(config)

    # Suscribirse al tema
    consumer.subscribe([topic])
    return consumer

def process_message(msg):
    # Procesar el mensaje recibido
    try:
        # Convertir el mensaje de Kafka a JSON
        record = json.loads(msg.value().decode('utf-8'))
        print("Mensaje recibido:", record)

        # Aquí puedes añadir la lógica de procesamiento de datos
        # Por ejemplo, análisis de datos, almacenamiento, etc.

    except json.decoder.JSONDecodeError as e:
        print("Error al decodificar el mensaje:", e)

def consume_messages(consumer):
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Fin de la partición
                    continue
                else:
                    print(msg.error())
                    break

            process_message(msg)

    except KeyboardInterrupt:
        pass
    finally:
        # Cerrar el consumidor
        consumer.close()

def main():
    # Configuración del consumidor
    kafka_config = {
        'bootstrap.servers': '127.0.0.1:9092',
        'group.id': 'mi_grupo',
        'auto.offset.reset': 'earliest'
    }

    topic = 'topic_bolsa'
    consumer = create_consumer(kafka_config, topic)
    consume_messages(consumer)

if __name__ == "__main__":
    main()


###########################       ENVIA DATOS A MONGO DB Y HACE CALCULOS CON ELLOS Y LOS PROCESA               ##################################

from confluent_kafka import Consumer, KafkaError
import json
from pymongo import MongoClient

# Conexión a MongoDB
def conectar_mongodb(uri="mongodb://localhost:27017"):
    client = MongoClient(uri)
    db = client['mi_base_datos']
    return db['mi_coleccion']

# Almacenamiento en MongoDB
def almacenar_en_mongodb(coleccion, data):
    coleccion.insert_one(data)

# Crear el consumidor de Kafka
def create_consumer(config, topic):
    consumer = Consumer(config)
    consumer.subscribe([topic])
    return consumer

# Procesar el mensaje recibido
def process_message(msg, coleccion_mongodb):
    try:
        record = json.loads(msg.value().decode('utf-8'))
        print("Mensaje recibido:", record)

        # Supongamos que queremos calcular el promedio de 'c' (precio de cierre)
        valor = record['c']
        almacenar_en_mongodb(coleccion_mongodb, {'precio_cierre': valor})

    except json.decoder.JSONDecodeError as e:
        print("Error al decodificar el mensaje:", e)


# Consumir mensajes de Kafka
def consume_messages(consumer, coleccion_mongodb):
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Fin de la partición, espera por más mensajes
                    continue
                else:
                    print(msg.error())
                    break

            process_message(msg, coleccion_mongodb)

    except KeyboardInterrupt:
        print("Interrumpido por el usuario")
    finally:
        consumer.close()
        print("Consumidor cerrado")


def main():
    kafka_config = {
        'bootstrap.servers': '127.0.0.1:9092',
        'group.id': 'mi_grupo',
        'auto.offset.reset': 'earliest'
    }

    topic = 'topic_bolsa'
    consumer = create_consumer(kafka_config, topic)
    coleccion_mongodb = conectar_mongodb()

    consume_messages(consumer, coleccion_mongodb)

if __name__ == "__main__":
    main()
