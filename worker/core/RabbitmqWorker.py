import json
import configparser

from asyncio import ProactorEventLoop
from pika import ConnectionParameters, PlainCredentials, BlockingConnection

from rabbitmq.Rabbitmq import Rabbitmq
from worker.service.WorkerService import WorkerService


class RabbitmqWorker(Rabbitmq):
    def __new__(cls):
        if not cls._instance:
            parser = configparser.ConfigParser()
            parser.read("../settings.ini")
            cls.__config = parser['rabbitmq']

            parameters = ConnectionParameters(
                host=cls.__config['rabbit_host'],
                virtual_host=cls.__config['rabbit_vhost'],
                port=int(cls.__config['rabbit_port']),
                credentials=PlainCredentials(cls.__config['rabbit_login'], cls.__config['rabbit_password']),
                heartbeat=600,
                blocked_connection_timeout=14400
            )

            cls._instance = super(RabbitmqWorker, cls).__new__(cls)

            cls.__connection = BlockingConnection(parameters)

            cls.__channel = cls.__connection.channel()

            cls.__channel.queue_bind(
                queue=cls.__config['input_queue'],
                exchange=cls.__config['out_exchange'],
                routing_key=cls.__config['input_queue']
            )

        return cls._instance

    @classmethod
    def listen(cls, loop: ProactorEventLoop = None):
        def input_callback(ch, method, properties, body):
            print(f" [x] Worker received from tgbot: {body}")

            message = WorkerService.run(body)

            cls.send(message)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        cls.__channel.basic_consume(
            queue=cls.__config['input_queue'],
            on_message_callback=input_callback
        )

        print('Worker listener is working, don\'t close this window!')
        cls.__channel.start_consuming()

    @classmethod
    def send(cls, data: json):
        cls.__channel.basic_publish(
            exchange=cls.__config['out_exchange'],
            routing_key=cls.__config['output_queue'],
            body=data)
        print("Your message has been send")