import pytest
from tests.factories import (BoardFactory, BoardParticipantFactory,
                             GoalCategoryFactory)


@pytest.mark.django_db
def test_category_id_get(client, test_user):

    bp = BoardParticipantFactory(set_auth_user=test_user)
    bp.board = BoardFactory()  # НЕ понмаю почему не работает SUBFACTORY
    bp.save()

    cat = GoalCategoryFactory(set_auth_user=test_user)
    cat.board = bp.board
    cat.save()

    client.login(username=test_user.username,
                 password='qwert123')
    response = client.get(f'/goals/goal_category/{cat.id}')

    print(f'### {response.data}')

    assert response.status_code == 200, 'Проблема получения данных'
    assert response.data['title'] == cat.title, 'Получены не корректные данные'


@pytest.mark.django_db
def test_category_id_patch(client, test_user):

    bp = BoardParticipantFactory(set_auth_user=test_user)
    bp.board = BoardFactory()  # НЕ понмаю почему не работает SUBFACTORY
    bp.save()

    cat = GoalCategoryFactory(set_auth_user=test_user)
    cat.board = bp.board
    cat.save()

    data = {
        'title': 'New Category Name',
    }
    client.login(username=test_user.username,
                 password='qwert123')
    response = client.patch(f'/goals/goal_category/{cat.id}',
                            data=data,
                            format='json',
                            content_type='application/json')

    print(f'### {response.data}')

    assert response.status_code == 200, 'Проблема получения данных'
    assert response.data['title'] == data['title'], 'Получены не корректные данные'


@pytest.mark.django_db
def test_category_id_delete(client, test_user):

    bp = BoardParticipantFactory(set_auth_user=test_user)
    bp.board = BoardFactory()  # НЕ понмаю почему не работает SUBFACTORY
    bp.save()

    cat = GoalCategoryFactory(set_auth_user=test_user)
    cat.board = bp.board
    cat.save()

    client.login(username=test_user.username,
                 password='qwert123')
    response = client.delete(f'/goals/goal_category/{cat.id}',
                             content_type='application/json')

    print(f'### {response.data}')

    assert response.status_code == 204, 'Проблема получения данных'
