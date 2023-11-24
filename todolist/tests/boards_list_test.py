import pytest
from tests.factories import (BoardFactory, BoardParticipantFactory,
                             GoalCategoryFactory)


@pytest.mark.django_db
def test_boards_emptylist(auth_client):
    """
    Проверяет список досок для вновь созданного пустого пользователя
    """

    response = auth_client.get('/goals/board/list')

    assert response.status_code == 200, 'Проблема получения пустого списка'
    assert len(response.data) == 0, 'Список НЕ пустой'


@pytest.mark.django_db
def test_boards_list(client, test_user):
    """
    Создаёт 10 досок для пользователя и пробует проверить их
    спикок. Должно быть 10 досок в результах выдачи
    """

    bps = BoardParticipantFactory.create_batch(10, set_auth_user=test_user)
    for bp in bps:
        bp.board = BoardFactory()
        bp.save()  # НЕ понимаю почему не работает без этого цикла...

    client.login(username=test_user.username,
                 password='qwert123')
    response = client.get('/goals/board/list')

    print(f'### {response.data}')
    for bp in bps:
        print(f'{bp.user.username} - {bp.board.title}')

    assert response.status_code == 200, 'Проблема получения списка'
    assert len(response.data) == 10, 'Длина списка не корректна'
