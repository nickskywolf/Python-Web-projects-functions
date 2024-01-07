from fastapi.testclient import TestClient

import main

fake_client = TestClient(main.app)


def test_root():
    """
    The test_root function tests the root route of our application.
    It does this by making a GET request to the '/' endpoint and then asserts that
    the response status code is 200, which means that it was successful.

    :return: A response object
    :doc-author: Trelent
    """
    response = fake_client.get('/')

    assert response.status_code == 200

