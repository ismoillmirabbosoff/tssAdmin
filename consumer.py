import pika, json, os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from companies.serializer import  CompanySerializer, SuperCompanySerializer, DeviceSerializer
from decouple import config

params = pika.URLParameters(config("AMPQ"))
connection = pika.BlockingConnection(params)
channel = connection.channel()
# channel.queue_declare(queue='admin', durable=True)


def callback(ch, method, properties, body):
    print('Received in admin') 
    data = json.loads(body)
    # if properties.content_type == 'saveDevice':
    #     print("saveDevice")
    #     data["company"] = data["companyID"]
    #     serializer = DeviceSerializer(data=data) 
        
    if properties.content_type == 'saveCompany':
        print("saveCompany")
        serializer = CompanySerializer(data=data)

    elif properties.content_type == 'updateCompany':
        print("updateCompany")
        serializer = CompanySerializer(data=data)

    elif properties.content_type == 'updateDevice':
        print("updateDevice")
        serializer = DeviceSerializer(data=data)

    elif properties.content_type == 'updateSuperCompany':
        print("updateSuperCompany")
        serializer = SuperCompanySerializer(data=data)

    print("Data",str(body))
    serializer.create_or_update(data)
    ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_consume(queue=config('AMPQ_QUEUE_RX'), on_message_callback=callback) #, auto_ack=True
print('Admin Started Consuming')
print("...")
channel.start_consuming()
channel.close()
 