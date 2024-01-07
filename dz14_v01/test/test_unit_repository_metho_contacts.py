import unittest
from unittest.mock import patch, MagicMock

from sqlalchemy.orm import Session

from src.database.db_models import ContactPerson, User
from src.valid_schemas import ContactPersonModel

from src.repository.metho_contacts import (
    rep_create_contact,
    rep_show_all_contacts,
    rep_show_contact,
    rep_update_contact,
    rep_remove_contact,
)


class TestMethoContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    def tearDown(self):
        
        del self.session
        del self.user

    async def test_create_contact(self):
        
        body = ContactPersonModel(
            name='Albert',
            surname='Einstein',
            email='genius@gmail.com',
            phone='+380888888888',
            b_date='1879-03-14',
            additional_info='Test info.',
        )

        result = await rep_create_contact(body=body, user=self.user, db=self.session)

        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.b_date, body.b_date)
        self.assertEqual(result.additional_info, body.additional_info)
        self.assertTrue(hasattr(result, "id"))

    async def test_rep_show_all_contacts(self):
        
        contacts = [ContactPerson(), ContactPerson(), ContactPerson()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await rep_show_all_contacts(skip=0, user=self.user, limit=2, db=self.session)
        self.assertEqual(result, contacts)

    async def test_rep_show_contact(self):
    
        contacts = [ContactPerson(id=1), ContactPerson(id=2), ContactPerson(id=3)]
        self.session.query().filter().first.return_value = contacts
        result = await rep_show_contact(id=1, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_rep_update_contact(self):
        
        basic_contact = ContactPerson(id=1)

        body = ContactPerson(
            name='Albert',
            surname='Einstein',
            email='genius@gmail.com',
            phone='+380888888888',
            b_date='1879-03-14',
            additional_info='Test info.',
        )

        self.session.query().filter().first.return_value = basic_contact

        result = await rep_update_contact(id=1, body=body, user=self.user, db=self.session)

        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.b_date, body.b_date)
        self.assertEqual(result.additional_info, body.additional_info)

    async def test_rep_remove_contact(self):
        
        var = ContactPerson(id=1, name='Lacmus')
        self.session.query().filter().first.return_value = var
        result = await rep_remove_contact(id=1, user=self.user, db=self.session)
        self.assertEqual(var, result)


if __name__ == '__main__':
    unittest.main()
