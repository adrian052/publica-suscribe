import pika
import sys
sys.path.append('../')
from monitor import Monitor
from utils.middlewares import Middlewares
import time

class ProcesadorAlarmaMedicamento:

    def consume(self):
        try:
            # Se establece la conexión con el Distribuidor de Mensajes
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            # Se solicita un canal por el cuál se enviarán los signos vitales
            channel = connection.channel()
            # Se declara una cola para leer los mensajes enviados por el
            # Publicador
            channel.queue_declare(queue='take_medicine', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(on_message_callback=self.callback, queue='take_medicine')
            channel.start_consuming()  # Se realiza la suscripción en el Distribuidor de Mensajes
        except (KeyboardInterrupt, SystemExit):
            channel.close()  # Se cierra la conexión
            sys.exit("Conexión finalizada...")
            time.sleep(1)
            sys.exit("Programa terminado...")

    def callback(self, ch, method, properties, body):
        json_message = Middlewares.string_to_json(body)
        monitor = Monitor()
        monitor.print_take_medicine(json_message['datetime'], json_message['id'], json_message[
                                       'medicine_to_take'], json_message['model'])
        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    

if __name__ == '__main__':
    p_take_medicine = ProcesadorAlarmaMedicamento()
    p_take_medicine.consume()