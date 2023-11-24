import factory
from django.contrib.auth import get_user_model
from factory import fuzzy
from goals.models import (Board, BoardParticipant, Goal, GoalCategory,
                          GoalComment)

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker('word')
    is_deleted = False


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant
        skip_postgeneration_save = True

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = BoardParticipant.Role.owner

    @factory.post_generation
    def set_auth_user(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            obj.user = extracted


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory
        skip_postgeneration_save = True

    board = factory.SubFactory(BoardFactory)
    title = factory.Faker('word')
    user = factory.SubFactory(UserFactory)
    is_deleted = False

    @factory.post_generation
    def set_auth_user(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            obj.user = extracted


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal
        skip_postgeneration_save = True

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    user = factory.SubFactory(UserFactory)
    status = Goal.Status.to_do
    priority = fuzzy.FuzzyChoice(choices=Goal.Priority.values)
    category = factory.SubFactory(GoalCategoryFactory)

    @factory.post_generation
    def set_auth_user(obj, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            obj.user = extracted
            obj.category.user = extracted


class GoalCommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = factory.Faker('sentence')
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
