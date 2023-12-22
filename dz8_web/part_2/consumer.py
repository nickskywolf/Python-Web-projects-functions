import pika
from model import Contact
import json


def send_email_stub(contact):
    print(f"Sending email to {contact.full_name} at {contact.email}")
    contact.message_sent = True
    try:
        contact.save()
    except Exception as e:
        print(f"Error updating contact: {e}")


def callback(ch, method, properties, body):
    contact_id = json.loads(body)
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_email_stub(contact)
    else:
        print("Contact not found")


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
queue_name = 'hw8 queue'
channel.queue_declare(queue=queue_name, durable=True)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
