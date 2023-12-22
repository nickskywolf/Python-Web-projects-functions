import json

from model import Contact
from faker import Faker
import pika

fake = Faker()
NUM_OF_CONTACTS = 10

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

exchange_name = 'hw8 exchange'
queue_name = 'hw8 queue'
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange_name, queue=queue_name)

if __name__ == '__main__':
    for i in range(NUM_OF_CONTACTS):
        fake_user = Contact(full_name=fake.name(), email=fake.email(), birth_date=fake.date_of_birth()).save()
        channel.basic_publish(exchange=exchange_name, routing_key=queue_name,
                              body=json.dumps(str(fake_user.id)).encode('utf-8'),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),)
    connection.close()
