from fastapi.testclient import TestClient

import main

fake_client = TestClient(main.app)


def test_root():
    
    response = fake_client.get('/')

    assert response.status_code == 200

