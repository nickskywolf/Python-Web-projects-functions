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
        """
        The setUp function is called before each test function.
        It creates a mock session object and a user object with an id of 1.

        :param self: Represent the instance of the class
        :return: Self
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    def tearDown(self):
        """
        The tearDown function is called after each test.
        It deletes the session and user objects created in setUp.

        :param self: Represent the instance of the class
        :return: The session and the user
        :doc-author: Trelent
        """
        del self.session
        del self.user

    async def test_create_contact(self):
        """
        The test_create_contact function tests the rep_create_contact function.
        It creates a ContactPersonModel object and passes it to the rep_create_contact function, along with a user and db session.
        The result is then compared to the original body object.

        :param self: Represent the instance of the class
        :return: A contactpersonmodel object with the same attributes as the body
        :doc-author: Trelent
        """
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
        """
        The test_rep_show_all_contacts function tests the rep_show_all_contacts function.
        It creates a list of ContactPerson objects, and assigns it to the return value of self.session.query().filter().offset().limit().all()
        The result is then compared to contacts, which should be equal.

        :param self: Represent the instance of the class
        :return: A list of contacts
        :doc-author: Trelent
        """
        contacts = [ContactPerson(), ContactPerson(), ContactPerson()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await rep_show_all_contacts(skip=0, user=self.user, limit=2, db=self.session)
        self.assertEqual(result, contacts)

    async def test_rep_show_contact(self):
        """
        The test_rep_show_contact function tests the rep_show_contact function.
        It does this by creating a mock session object, and then mocking the query method of that object.
        The filter method is also mocked, as well as first(). The return value of first() is set to contacts.
        Then we call rep_show_contact with an id= 1 and user = self.user (which was created in setUp).
        We assert that result == contacts.

        :param self: Represent the instance of the class
        :return: The contacts list
        :doc-author: Trelent
        """
        contacts = [ContactPerson(id=1), ContactPerson(id=2), ContactPerson(id=3)]
        self.session.query().filter().first.return_value = contacts
        result = await rep_show_contact(id=1, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_rep_update_contact(self):
        """
        The test_rep_update_contact function tests the rep_update_contact function.
        It does so by creating a basic contact, then creating a body with new values for that contact.
        The session is then mocked to return the basic contact when queried, and the result of calling
        rep_update_contact is compared to what we expect it should be.

        :param self: Represent the instance of the class
        :return: A contact with updated information
        :doc-author: Trelent
        """
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
        """
        The test_rep_remove_contact function tests the rep_remove_contact function.
        The test is successful if the result of calling rep_remove_contact with id= 1 and user = self.user, db = self.session
        is equal to var.

        :param self: Represent the instance of the class
        :return: The contact that was removed from the database
        :doc-author: Trelent
        """
        var = ContactPerson(id=1, name='Lacmus')
        self.session.query().filter().first.return_value = var
        result = await rep_remove_contact(id=1, user=self.user, db=self.session)
        self.assertEqual(var, result)


if __name__ == '__main__':
    unittest.main()
