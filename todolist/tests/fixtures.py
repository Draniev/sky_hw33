from django.test import Client
import pytest


@pytest.fixture()
@pytest.mark.django_db
def auth_client(django_user_model):
    """
    Возвращает аутентифицированный объект Client
    для тестирования методов, доступных только для
    аутентифицированных пользователей.
    """
    username = 'test_user'
    password = 'qwert123'
    email = 'test_user@test.ru'

    django_user_model.objects.create_user(
        username=username,
        password=password,
        email=email,
    )

    client = Client()
    client.login(username=username, password=password)
    return client


@pytest.fixture()
@pytest.mark.django_db
def test_user(django_user_model):
    username = 'test_user'
    password = 'qwert123'
    email = 'test_user@test.ru'

    user = django_user_model.objects.create_user(
        username=username,
        password=password,
        email=email,
    )

    return user
