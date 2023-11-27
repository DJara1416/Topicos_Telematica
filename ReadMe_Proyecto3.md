# Proyecto de Procesamiento en Tiempo Real de Datos de la Bolsa
## Integrantes
1. Antonio Carmona Gaviria
2. Kevin Sossa Chavarria
3. Jacobo Rave Londoño
4. Daniel Jaramillo Valencia 

## Descripción
Este proyecto se enfoca en capturar datos en tiempo real de la bolsa de valores utilizando una API gratuita, procesar estos datos utilizando Apache Kafka y Pyhtond Streaming, y almacenar los resultados en MongoDB para su análisis y visualización.

## Requisitos Previos
- Python 3.x
- Apache Kafka
- MongoDB
- Cuenta de API para datos de la bolsa de valores
- Conocimientos básicos en Python, Kafka, Spark y MongoDB

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

## Procesamiento de Datos con Python para Streaming
1. **Script de Procesamiento con Python**:
    - Desarrollar un script en Python que lea datos del tema de Kafka.
    - Realizar operaciones de procesamiento o análisis en los datos (por ejemplo, cálculos de promedios móviles).
    - Almacenar los resultados del análisis en MongoDB.

## Visualización de Datos
1. **Configuración de Herramientas de Visualización**:
    - Instalar y configurar Apache Superset o una herramienta similar.
    - Conectar la herramienta con MongoDB para visualizar los datos en tiempo real.

## Uso y Mantenimiento
1. **Ejecutar los Scripts Regularmente**:
    - Asegurarse de que el script de captura de datos y el script de Python estén ejecutándose continuamente.

2. **Monitoreo y Mantenimiento**:
    - Monitorear el sistema regularmente para asegurarse de que todo funcione correctamente.
    - Realizar mantenimiento y actualizaciones según sea necesario.

## Consideraciones Finales
- Este proyecto es para fines educativos y de desarrollo. Para un entorno de producción, se deben considerar aspectos como la escalabilidad, la gestión de errores y la seguridad.
- Familiarízate con las limitaciones de la API de la bolsa y asegúrate de cumplir con sus términos de uso.
