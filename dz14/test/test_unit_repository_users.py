import unittest
from unittest.mock import patch, MagicMock, Mock, create_autospec

from sqlalchemy.orm import Session

from src.database.db_models import User, ContactPerson
from src.valid_schemas import UserModel

import src.repository.users
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

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

    async def test_get_user_by_email(self):
        """
        The test_get_user_by_email function tests the get_user_by_email function.
        It does this by creating a mock ContactPerson object, and then setting the return value of
        the session's query().filter().first() method to be that mock object. Then it calls the
        get_user_by_email function with an email address matching that of our test entity, and checks
        that it returns our test entity.

        :param self: Refer to the current instance of a class
        :return: The test_entity
        :doc-author: Trelent
        """
        email = 'test@mail.box'
        test_entity = ContactPerson(email=email)
        self.session.query().filter().first.return_value = test_entity
        result = await get_user_by_email(email=email, db=self.session)
        self.assertEqual(result, test_entity)

    async def test_create_user(self):
        """
        The test_create_user function tests the create_user function in the user.py file.
        It creates a new UserModel object with username, email and password fields, then passes it to
        the create_user function along with a database session object (self.session). The result is
        then compared to the original body of data that was passed into the create_user function.

        :param self: Refer to the instance of the class
        :return: An object of the usermodel class
        :doc-author: Trelent
        """
        body = UserModel(
            username='Albert',
            email='test@mail.box',
            password='XXXXXX'
        )

        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.password, body.password)
        self.assertEqual(result.email, body.email)

    async def test_update_token(self):
        """
        The test_update_token function tests the update_token function in the database.py file.
        It does this by creating a user, and then updating that user's refresh token to 'TOKEN'.
        The test passes if the new refresh token is equal to 'TOKEN'.

        :param self: Represent the instance of the class
        :return: The token that was passed in
        :doc-author: Trelent
        """
        token = 'TOKEN'
        result = await update_token(user=self.user, token=token, db=self.session)
        self.assertEqual(token, self.user.refresh_token)


    @patch.object(src.repository.users, 'get_user_by_email')
    async def test_confirmed_email(self, mock_get_user_by_email):
        """
        The test_confirmed_email function tests the confirmed_email function.
        It mocks the get_user_by_email function to return a user object, and then calls the confirmed email function with that user's email address.
        The test asserts that get_user by email was called once, and also asserts that after calling confirmed email,
        the returned user is marked as having a confirmed account.

        :param self: Access the attributes and methods of the class
        :param mock_get_user_by_email: Mock the get_user_by_email function
        :return: True
        :doc-author: Trelent
        """
        mock_get_user_by_email.return_value = self.user
        email = 'test@mail.box'

        result = await confirmed_email(email=email, db=self.session)
        mock_get_user_by_email.assert_called_once()
        self.assertTrue(self.user.confirmed)

    @patch.object(src.repository.users, 'get_user_by_email')
    async def test_update_avatar(self, mock_get_user_by_email):
        """
        The test_update_avatar function tests the update_avatar function.
        It does so by mocking the get_user_by_email function, which is called in update_avatar.
        The test then asserts that the mocked user's avatar attribute has been updated to match url.

        :param self: Access the instance of the class
        :param mock_get_user_by_email: Mock the get_user_by_email function
        :return: The user's avatar
        :doc-author: Trelent
        """
        mock_get_user_by_email.return_value = self.user
        email = 'test@mail.box'
        url = 'test_url'

        result = await update_avatar(email=email, url=url, db=self.session)
        mock_get_user_by_email.assert_called_once()
        self.assertEqual(url, self.user.avatar)




if __name__ == '__main__':
    unittest.main()
