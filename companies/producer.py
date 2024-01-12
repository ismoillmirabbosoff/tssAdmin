
import pika, json
from json import JSONEncoder
from uuid import UUID
from decouple import config

JSONEncoder_olddefault = JSONEncoder.default
def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)
JSONEncoder.default = JSONEncoder_newdefault

params = pika.URLParameters(config("AMPQ"))
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue=config('AMPQ_QUEUE_TX_T'), durable=True)
channel.queue_declare(queue=config('AMPQ_QUEUE_TX_M'), durable=True)
# def publish(body):
#     channel.basic_publish(exchange='',routing_key='admin',body=body)


def publish(method, body,routingKey):
    print("publishing...")
    print(body)
    print(routingKey)
    try:
        connection = pika.BlockingConnection(params)
        properties = pika.BasicProperties(method)
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=routingKey, body=json.dumps(body), properties=properties)
    except Exception as e:
        print(e)
        connection = pika.BlockingConnection(params)
        properties = pika.BasicProperties(method)
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=routingKey, body=json.dumps(body), properties=properties)



# publish()


