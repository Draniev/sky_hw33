import pytest


def test_update_password(auth_client):
    old_password = 'qwert123'
    new_password = 'newtestpassword'
    data = {
        'old_password': old_password,
        'new_password': new_password
    }

    # Make the request
    response = auth_client.patch('/core/update_password',
                                 data=data,
                                 format='json',
                                 content_type='application/json',)

    # Check the response code
    assert response.status_code == 200
