import pytest
from tests.factories import BoardFactory, BoardParticipantFactory, GoalFactory, GoalCategoryFactory


@pytest.mark.django_db
def test_goal_create(client, test_user):

    board = BoardFactory()
    boardparticipant = BoardParticipantFactory(set_auth_user=test_user)
    boardparticipant.board = board
    boardparticipant.save()

    category = GoalCategoryFactory(set_auth_user=test_user)
    category.board = board
    category.save()

    client.login(username=test_user.username,
                 password='qwert123')
    data = {
        'title': 'Тестовая цель',
        'description': 'Какое то описание цели',
        'category': category.id
    }

    response = client.post('/goals/goal/create',
                           data=data,
                           format='json')

    print(f'### {response.data}')
    assert response.status_code == 201, 'Неверный статус-код создания цели'
    # assert len(response.data) == 10, 'Длина списка не корректна'
