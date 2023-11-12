from django.contrib.auth import get_user_model
from django.db import models
from goals.models import GoalCategory

User = get_user_model()


class TgUser(models.Model):
    class Meta:
        verbose_name = "Пользователь ТГ"
        verbose_name_plural = "Пользователи ТГ"

    class State(models.IntegerChoices):
        not_confirmed = 1, "Ожидаем подтверждения"
        confirmed = 2, "Подтверждён"
        create_1 = 3, "Ждём категорию"
        create_2 = 4, "Ждём название"

    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, verbose_name="Пользователь",
                             null=True,
                             on_delete=models.PROTECT)
    state = models.PositiveSmallIntegerField(verbose_name='Состояние',
                                             choices=State.choices,
                                             default=State.not_confirmed)
    verification_code = models.CharField(verbose_name='Код авторизации',
                                         max_length=255, null=True)
    create_goal_category = models.ForeignKey(GoalCategory,
                                             verbose_name="Категория для создания цели",
                                             null=True,
                                             on_delete=models.PROTECT)
