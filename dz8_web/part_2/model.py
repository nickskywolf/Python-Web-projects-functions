from mongoengine import StringField, DateField, Document, connect, BooleanField

connect(db='hw8',
        host='mongodb+srv://mihanch:*****@cluster0.xo49jrs.mongodb.net/')


class Contact(Document):
    full_name = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True)
    message_sent = BooleanField(required=True, default=False)
    birth_date = DateField()
    meta = {'collection': 'contacts'}


