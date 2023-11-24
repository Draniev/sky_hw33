import pytest
from tests.factories import BoardFactory, BoardParticipantFactory


@pytest.mark.django_db
def test_goal_create(client, test_user):

    board = BoardFactory()
    boardparticipant = BoardParticipantFactory(set_auth_user=test_user)
    boardparticipant.board = board
    boardparticipant.save()

    client.login(username=test_user.username,
                 password='qwert123')
    data = {
        'title': 'Тестовая категория',
        'board': board.id
    }

    response = client.post('/goals/goal_category/create',
                           data=data,
                           format='json')

    print(f'### {response.data}')
    assert response.status_code == 201, 'Неверный статус-код создания категории'

    response = client.get('/goals/goal_category/list')

    assert response.status_code == 200, 'Неверный статус-код создания категории'
    assert len(response.data) == 1
