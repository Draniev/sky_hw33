import pytest


def test_server_on(client):
    response = client.get('/')
    assert response.status_code == 404
