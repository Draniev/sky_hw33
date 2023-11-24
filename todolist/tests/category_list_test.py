import pytest
from tests.factories import (BoardFactory, BoardParticipantFactory,
                             GoalCategoryFactory)


@pytest.mark.django_db
def test_goals_emptylist(auth_client):
    """
    Проверяет список целей для вновь созданного пустого пользователя
    """

    response = auth_client.get('/goals/goal_category/list')

    assert response.status_code == 200, 'Проблема получения пустого списка'
    assert len(response.data) == 0, 'Список НЕ пустой'


@pytest.mark.django_db
def test_goals_list(client, test_user):
    """
    Создаёт 10 целей для конкретного пользователя и пробует проверить их
    спикок. долго быть 10 целей в результах выдачи
    """

    # Создаёт доску в которой конкретный пользователь
    # является создателем
    board = BoardFactory()
    boardparticipant = BoardParticipantFactory(set_auth_user=test_user)
    boardparticipant.board = board
    boardparticipant.save()

    categories = GoalCategoryFactory.create_batch(10, set_auth_user=test_user)
    for category in categories:
        category.board = board
        category.save()

    client.login(username=test_user.username,
                 password='qwert123')
    response = client.get('/goals/goal_category/list')

    print(f'### {response.data}')
    assert response.status_code == 200, 'Проблема получения списка'
    assert len(response.data) == 10, 'Длина списка не корректна'
