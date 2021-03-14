import pika
import sys
sys.path.append('../')
from monitor import Monitor
from utils.middlewares import Middlewares
import time


class ProcesadorAcelerometro:

    def consume(self):
        try:
            # Se establece la conexión con el Distribuidor de Mensajes
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            # Se solicita un canal por el cuál se enviarán los signos vitales
            channel = connection.channel()
            # Se declara una cola para leer los mensajes enviados por el
            # Publicador
            channel.queue_declare(queue='accelerometer', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(on_message_callback=self.callback, queue='accelerometer')
            channel.start_consuming()  # Se realiza la suscripción en el Distribuidor de Mensajes
        except (KeyboardInterrupt, SystemExit):
            channel.close()  # Se cierra la conexión
            sys.exit("Conexión finalizada...")
            time.sleep(1)
            sys.exit("Programa terminado...")

    def callback(self, ch, method, properties, body):
        json_message = Middlewares.string_to_json(body)
        pos_x = float(json_message['x_position'])
        pos_y = float(json_message['y_position'])
        pos_z = float(json_message['z_position'])

        if self.fall_down(pos_x, pos_y, pos_z) :
            monitor = Monitor()
            monitor.print_fall_down(json_message['datetime'], json_message['id'], json_message[
                                       'x_position'],json_message[
                                       'y_position'],json_message[
                                       'z_position'], json_message['model'])
        time.sleep(1)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def fall_down(self, position_x, position_y, position_z):
        if position_x > 0.5 and position_z < 0.1:
            return True
        if position_x < 0.5 and position_z < 0.3:
            return True
        return False
        

if __name__ == '__main__':
    p_acelerometro = ProcesadorAcelerometro()
    p_acelerometro.consume()