from xiaomi_my_band import XiaomiMyBand
import pika
import random
import time


class XiaomiMyBand2021(XiaomiMyBand):
    def __init__(self, id):
        self.software_version = "11.2.3.1"
        self.hardwar_version = "3.0.1.9.1"
        self.model = "Xiaomi My Band 3"
        self.id = id

    def publish(self):
        super(XiaomiMyBand2021, self).publish()
        self.publish_accelerometer()
        time.sleep(1)
        self.publish_time_take_medicine()
        time.sleep(1)

    def publish_accelerometer(self):
        message = {}
        message['x_position'] = self.simulate_x_position()
        message['y_position'] = self.simulate_y_position()
        message['z_position'] = self.simulate_z_position()
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        # Se declara una cola para persistir los mensajes enviados
        channel.queue_declare(queue='accelerometer', durable=True)
        channel.basic_publish(exchange='', routing_key='accelerometer', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión

    def publish_time_take_medicine(self):
        message = {}
        message['medicine_to_take'] = self.get_random_medicine()
        message['id'] = str(self.id)
        message['datetime'] = self.simulate_datetime()
        message['producer'] = self.producer
        message['model'] = self.model
        message['hardware_version'] = self.hardware_version
        message['software_version'] = self.software_version
        # Se establece la conexión con el Distribuidor de Mensajes
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # Se solicita un canal por el cuál se enviarán los signos vitales
        channel = connection.channel()
        # Se declara una cola para persistir los mensajes enviados
        channel.queue_declare(queue='take_medicine', durable=True)
        channel.basic_publish(exchange='', routing_key='take_medicine', body=str(message), properties=pika.BasicProperties(
            delivery_mode=2,))  # Se realiza la publicación del mensaje en el Distribuidor de Mensajes
        connection.close()  # Se cierra la conexión

    def get_random_medicine(self):
        medicines = ['paracetamol','ibuprofeno','naproxeno','fluxetina','insulina','furosemida', 'piroxicam', 'tolbutamida']
        return medicines[int(random.uniform(0, len(medicines)))]