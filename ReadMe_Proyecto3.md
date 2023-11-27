# Proyecto de Procesamiento en Tiempo Real de Datos de la Bolsa
## Integrantes

1. Antonio Carmona Gaviria
2. Kevin Sossa Chavarria
3. Jacobo Rave Londoño
4. Daniel Jaramillo Valencia 

## Descripción
Este proyecto se enfoca en capturar datos en tiempo real de la bolsa de valores utilizando una API gratuita, procesar estos datos utilizando Apache Kafka y Pyhton Streaming, y almacenar los resultados en MongoDB para su análisis y visualización.

## Requisitos Previos
- Python 3.x
- Apache Kafka
- MongoDB
- Cuenta de API para datos de la bolsa de valores
- Conocimientos básicos en Python, Kafka y MongoDB

## Configuración del Entorno
1. **Actualizacion del Sistema y Herramientas Básicas**:
    - Primero, actualiza tu sistema con los siguientes comandos y asegúrate de tener instaladas herramientas básicas como wget y unzip.
    ```
        sudo apt-get update
        sudo apt-get upgrade
        sudo apt-get install wget unzip
    ```
2. **Instalar Dependencias de Python**:
    - Instala Python y las bibliotecas necesarias para tu proyecto.
        ``` 
        sudo apt-get install python3 python3-pip 
        pip3 install kafka-python pymongo requests
        ``` 

3. **Configuración e Instalación de Apache Kafka**:
    - Instalación de Java (Requerido por Kafka)
        ``` 
         sudo apt install default-jre
        ``` 
    - Descargar e instalar Apache Kafka.
        ``` 
        wget https://archive.apache.org/dist/kafka/2.7.0/kafka_2.13-2.7.0.tgz
        tar -xzf kafka_2.13-2.7.0.tgz
        cd kafka_2.13-2.7.0
        ``` 
    - Iniciar Zookeeper y el servidor Kafka.
        ``` 
        bin/zookeeper-server-start.sh config/zookeeper.properties
        bin/kafka-server-start.sh config/server.properties
        ``` 
    - Crear un tema (topic) en Kafka para los datos de la bolsa.

4. **Configuración de MongoDB**:
    - Instalar MongoDB y ejecutar el servicio.
         ``` 
         sudo apt-get install -y mongodb
         sudo systemctl start mongodb
         sudo systemctl enable mongodb
        ``` 
    - Crear una base de datos y colección para almacenar los datos procesados.

5. **Verificación y Pruebas**
    - Verifica que Python y las bibliotecas están correctamente instaladas ejecutando python3 --version y pip3 list.
    - Para Kafka, crea un tema de prueba y prueba producir y consumir mensajes, con el siguientye codigo podras tener una     idea de como hacer una prueba de conexion, consumo de nuestra api y el envío de datos a KAFKA
      ```py
      from kafka import KafkaProducer
        import requests
        import json

        def obtener_datos_accion(symbol):
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token=API_KEY" ##### CAMBIA TU API KEY AQUI
            response = requests.get(url)
            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))
            else:
                return None
        
        # Ejemplo de uso
        datos = obtener_datos_accion("BINANCE:BTCUSDT")
        
        # Configuración del productor de Kafka
        producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        
        def enviar_datos_kafka(topic, data):
            producer.send(topic, data)
            producer.flush()
            print("Datos enviados a Kafka")
        
        # Enviar datos de la acción a Kafka
        enviar_datos_kafka("topic_bolsa", datos)
      ```
    - Verifica que MongoDB está funcionando correctamente conectándote a él con el cliente de MongoDB, con el siguinete       codigo podras verificar esta conexion mediante la impresion de los mensajes que lleguen desde KAFKA 
    ```py
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
    ```

## Captura de Datos
1. **Script de Captura de Datos de la Bolsa**:
    - Escribir un script en Python que use la API de la bolsa para obtener datos en tiempo real.
    - Publicar los datos capturados en el tema de Kafka creado anteriormente.
    -Para lo anteriror utlizaremos el siguiente scrip que lo que hace es todo el tema de conexion de la API de la bolsa, otencion y envio de datos 
    ```py
    from kafka import KafkaProducer
    import requests
    import json
    import time
    
    def obtener_datos_accion(symbol, api_key):
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return None
    
    def enviar_datos_kafka(topic, data, producer):
        producer.send(topic, data)
        producer.flush()
        print("Datos enviados a Kafka")
    
    def main():
        # Configuración del productor de Kafka
        producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
        api_key = "TU_API_KEY" # CAMBIA TU API KEY AQUI
        symbol = "BINANCE:BTCUSDT"
    
        while True:
            # Obtener datos de la API
            datos = obtener_datos_accion(symbol, api_key)
    
            if datos:
                # Enviar datos de la acción a Kafka
                enviar_datos_kafka("topic_bolsa", datos, producer)
            
            # Esperar X segundos antes de hacer la siguiente solicitud
            time.sleep(60)  # Puedes ajustar este intervalo según tus necesidades
    
    if __name__ == "__main__":
        main()

    ```
    En este script, la función main() ejecuta un bucle infinito que hace una solicitud a la API de Finnhub cada 60 segundos (este intervalo puede ser ajustado según tus necesidades). Los datos obtenidos son enviados a un tema de Kafka.
   
## Procesamiento de Datos con Python para Streaming
1. **Script de Procesamiento con Python**:
    - Desarrollar un script en Python que lea datos del tema de Kafka.
    - Realizar operaciones de procesamiento o análisis en los datos (por ejemplo, cálculos de promedios móviles).
    - Almacenar los resultados del análisis en MongoDB.
    - con el siguiente script en python se ahra toda la lectura y procesamiento de los datos ademas de aamacenarlos en la abse de datos, en este caso en MongoDB

   ```py
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
    ```
      - Explicación del Script
        - Conexión a MongoDB: El script se conecta a una base de datos MongoDB y especifica una colección donde se almacenarán los datos.
        - Consumidor de Kafka: Se crea un consumidor de Kafka que se suscribe a un tema específico.
        - Procesamiento de Mensajes: Cada mensaje recibido se decodifica de JSON. En este ejemplo, se extrae el valor del precio de cierre ('c') y se almacena en MongoDB.
        - Bucle Principal: El script entra en un bucle que lee mensajes de Kafka y los procesa continuamente.
      
## Visualización de Datos 
1. **Descripción**:
    - La visualización de los datos que tendremos en el proyecto sera a traves de Mongo Altlas, lo cual permite ser  más productivos con nuestros datos.

## Uso y Mantenimiento
1. **Ejecutar los Scripts Regularmente**:
    - Asegurarse de que el script de captura de datos y el script de Python estén ejecutándose continuamente.

2. **Monitoreo y Mantenimiento**:
    - Monitorear el sistema regularmente para asegurarse de que todo funcione correctamente.
    - Realizar mantenimiento y actualizaciones según sea necesario.

