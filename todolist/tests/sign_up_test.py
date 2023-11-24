import pytest


@pytest.mark.django_db
def test_sign_up(client):
    data = {
        'username': 'test_user',
        'password': 'qwfpg123',
        'password_repeat': 'qwfpg123',
    }

    response = client.post(
        '/core/signup',
        data=data,
        format='json',
    )

    print(response.data)
    assert response.status_code == 201, 'Проблема при создании пользователя'
