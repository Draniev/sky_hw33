import pytest
from tests.factories import (BoardFactory, BoardParticipantFactory,
                             GoalCategoryFactory, GoalFactory)


@pytest.mark.django_db
def test_goal_id_get(client, test_user):

    bp = BoardParticipantFactory(set_auth_user=test_user)
    bp.board = BoardFactory()  # НЕ понмаю почему не работает SUBFACTORY
    bp.save()

    cat = GoalCategoryFactory(set_auth_user=test_user)
    cat.board = bp.board
    cat.save()

    goal = GoalFactory(set_auth_user=test_user)
    goal.category = cat
    goal.save()

    client.login(username=test_user.username,
                 password='qwert123')
    response = client.get(f'/goals/goal/{goal.id}')

    print(f'### {response.data}')

    assert response.status_code == 200, 'Проблема получения данных'
    assert response.data['title'] == goal.title, 'Получены не корректные данные'


@pytest.mark.django_db
def test_category_id_patch(client, test_user):

    bp = BoardParticipantFactory(set_auth_user=test_user)
    bp.board = BoardFactory()  # НЕ понмаю почему не работает SUBFACTORY
    bp.save()

    cat = GoalCategoryFactory(set_auth_user=test_user)
    cat.board = bp.board
    cat.save()

    goal = GoalFactory(set_auth_user=test_user)
    goal.category = cat
    goal.save()

    data = {
        'title': 'New Goal Name',
    }
    client.login(username=test_user.username,
                 password='qwert123')
    response = client.patch(f'/goals/goal/{goal.id}',
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

    goal = GoalFactory(set_auth_user=test_user)
    goal.category = cat
    goal.save()

    client.login(username=test_user.username,
                 password='qwert123')
    response = client.delete(f'/goals/goal/{goal.id}',
                             content_type='application/json')

    print(f'### {response.data}')

    assert response.status_code == 204, 'Проблема получения данных'
