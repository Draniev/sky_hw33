from django.db.models import Q
from bot.models import TgUser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import  permissions
from rest_framework.generics import UpdateAPIView
from bot.serializers import CategoryList4TgSerializer, GoalList4TgSerializer, TgUserUpdSerializer
from bot.tg.client import TgClient
from goals.models import BoardParticipant, Goal, GoalCategory
from todolist.settings import TG_TOKEN


@method_decorator(ensure_csrf_cookie, name='dispatch')
class BotUserVerifyView(UpdateAPIView):
    model = TgUser
    # lookup_field = 'verification_code'
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserUpdSerializer

    def get_queryset(self):
        verification_code = self.request.data.get('verification_code')
        return TgUser.objects.filter(verification_code=verification_code)

    def get_object(self):
        queryset = self.get_queryset()

        try:
            return queryset.first()
        except TgUser.DoesNotExist:
            # Handle the case where the object is not found
            raise Http404("No TgUser matches the given query.")

    def perform_update(self, serializer):
        tg_user = self.get_object()
        chat_id = tg_user.chat_id
        tg_client = TgClient(TG_TOKEN)
        tg_client.send_message(chat_id, "Верификация выполнена.")
        return super().perform_update(serializer)


def goals_list_4_tg(tg_user: TgUser) -> str:
    # Список всех досок пользователя
    boards = BoardParticipant.objects.filter(user=tg_user.user).values('board')

    # кверисет всех целей, своих и доступных на чужих досках
    goals = Goal.objects.filter(
        Q(user=tg_user.user, status__in=[1, 2, 3]) |
        # Цели, состоящие в досках к которым есть доступ
        Q(category__in=GoalCategory.objects.filter(board__in=boards),
          status__in=[1, 2, 3])
    )

    serializer = GoalList4TgSerializer(goals, many=True)
    if len(serializer.data):
        str = ", ".join([goal['title'] for goal in serializer.data])
        str = "Ваши цели:\n" + str
    else:
        str = "Не удалось найти ни одной цели. Может создадим первую?"

    return str


def get_goal_categories(tg_user: TgUser) -> list[str]:
    categoryes = GoalCategory.objects.filter(
        Q(user=tg_user.user, is_deleted=False) |
        # Категории, у которых доска, в которой пользователь состоит
        Q(board__in=BoardParticipant.objects.filter(user=tg_user.user).values('board'),
          is_deleted=False)
    )

    serializer = CategoryList4TgSerializer(categoryes, many=True)
    return [category['title'] for category in serializer.data]


def get_goal_category(tg_user: TgUser, category_name: str) -> GoalCategory:
    categoryes = GoalCategory.objects.filter(
        Q(user=tg_user.user, is_deleted=False) |
        # Категории, у которых доска, в которой пользователь состоит
        Q(board__in=BoardParticipant.objects.filter(user=tg_user.user).values('board'),
          is_deleted=False)
    )

    return categoryes.get(title=category_name)


def create_goal_from_tg(tg_user: TgUser, title: str):
    goal = Goal(user=tg_user.user,
                category=tg_user.create_goal_category,
                title=title)
    goal.save()
    return goal
