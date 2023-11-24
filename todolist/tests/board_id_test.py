import pytest
from tests.factories import (BoardFactory, BoardParticipantFactory)


@pytest.mark.django_db
def test_board_id_get(client, test_user):

    bp = BoardParticipantFactory(set_auth_user=test_user)
    bp.board = BoardFactory()  # НЕ понмаю почему не работает SUBFACTORY
    bp.save()

    client.login(username=test_user.username,
                 password='qwert123')
    response = client.get(f'/goals/board/{bp.board.id}')

    print(f'### {response.data}')
    print(f'{bp.user.username} - {bp.board.title}')

    assert response.status_code == 200, 'Проблема получения данных'
    assert response.data['title'] == bp.board.title, 'Получены не корректные данные'
