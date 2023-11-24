import pytest
from tests.factories import BoardFactory, BoardParticipantFactory


@pytest.mark.django_db
def test_goal_create(client, test_user):

    client.login(username=test_user.username,
                 password='qwert123')
    data = {
        'title': 'Тестовая доска',
    }

    response = client.post('/goals/board/create',
                           data=data,
                           format='json')

    print(f'### {response.data}')
    assert response.status_code == 201, 'Неверный статус-код создания доски'

    response = client.get('/goals/board/list')
    print(f'### {response.data}')
    assert response.status_code == 200, 'Неверный статус-код создания доски'
    assert len(response.data) == 1
