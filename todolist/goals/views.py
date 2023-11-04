from django.db.models import Q
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters.rest_framework import DjangoFilterBackend
from goals.filters import GoalDateFilter
from goals.models import Board, BoardParticipant, Goal, GoalCategory, GoalComment
from goals.permissions import BoardPermissions, CategoryPermissions, CategoryCreatePermission, CommentCreatePermission, CommentPermissions
from goals.serializers import (BoardCreateSerializer,
                               GoalCategoryCreateSerializer,
                               GoalCategorySerializer,
                               GoalCommentCreateSerializer,
                               GoalCommentSerializer, GoalCreateSerializer,
                               GoalSerializer, BoardSerializer, BoardListSerializer)
from rest_framework import filters, permissions
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.pagination import LimitOffsetPagination


@method_decorator(ensure_csrf_cookie, name='dispatch')
class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class BoardListView(ListAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user, is_deleted=False
        )


@method_decorator(ensure_csrf_cookie, name='dispatch')
class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated, CategoryCreatePermission]
    serializer_class = GoalCategoryCreateSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title", "board"]
    search_fields = ["title", "board"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            Q(user=self.request.user, is_deleted=False) |
            # Категории, у которых доска, в которой пользователь состоит
            Q(board__in=BoardParticipant.objects.filter(user=self.request.user).values('board'),
              is_deleted=False)
        )


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, CategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            Q(user=self.request.user, is_deleted=False) |
            # Категории, у которых доска, в которой пользователь состоит
            Q(board__in=BoardParticipant.objects.filter(user=self.request.user).values('board'),
              is_deleted=False)
        )

    def perform_destroy(self, instance):
        # Update the status of associated Goal objects to 4 (archived)
        associated_goals = Goal.objects.filter(category=instance)
        associated_goals.update(status=4)

        # Soft-delete the GoalCategory
        instance.is_deleted = True
        instance.save()

        return instance


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        user_boards = BoardParticipant.objects.filter(user=self.request.user).values('board')

        return Goal.objects.filter(
            Q(user=self.request.user, status__in=[1, 2, 3]) |
            # Цели, состоящие в досках к которым есть доступ
            Q(category__in=GoalCategory.objects.filter(board__in=user_boards),
              status__in=[1, 2, 3])
            )


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_boards = BoardParticipant.objects.filter(user=self.request.user).values('board')

        return Goal.objects.filter(
            Q(user=self.request.user, status__in=[1, 2, 3]) |
            # Цели, состоящие в досках к которым есть доступ
            Q(category__in=GoalCategory.objects.filter(board__in=user_boards),
              status__in=[1, 2, 3])
            )

    def perform_destroy(self, instance):
        instance.status = 4
        instance.save()
        return instance


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated, CommentCreatePermission]
    serializer_class = GoalCommentCreateSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCommentListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ["created"]
    ordering = ["text"]

    def get_queryset(self):
        user_boards = BoardParticipant.objects.filter(user=self.request.user).values('board')

        return GoalComment.objects.filter(
            Q(user=self.request.user) |
            # Цели, состоящие в досках к которым есть доступ
            Q(goal__in=Goal.objects.filter(category__in=GoalCategory.objects.filter(board__in=user_boards)))
            )


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentPermissions]

    def get_queryset(self):
        user_boards = BoardParticipant.objects.filter(user=self.request.user).values('board')

        return GoalComment.objects.filter(
            Q(user=self.request.user) |
            # Цели, состоящие в досках к которым есть доступ
            Q(goal__in=Goal.objects.filter(category__in=GoalCategory.objects.filter(board__in=user_boards)))
            )
