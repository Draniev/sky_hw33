import pytest


@pytest.mark.django_db
def test_login(client, test_user):
    data = {
        'username': test_user.username,
        'password': 'qwert123',
    }

    response = client.post(
        '/core/login',
        data=data,
        format='json',
    )

    print(response.data)
    assert response.status_code == 201, 'Проблема при входе в аккаунт'
    assert response.data['username'] == test_user.username


@pytest.mark.django_db
def test_profile(client, test_user):

    client.login(username=test_user.username,
                 password='qwert123')
    response = client.get('/core/profile')

    print(response.data)
    assert response.status_code == 200, 'Проблема при входе в профиль'
    assert response.data['username'] == test_user.username
