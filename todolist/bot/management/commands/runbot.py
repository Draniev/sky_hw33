from random import randint
from typing import Tuple

from bot.management.commands.dialogs import (BAD_CATEGORY, BAD_COMMAND,
                                             CODE_DESCRIPTION, CREATE_2, CREATE_BRAKE, CREATE_SUCCESS,
                                             GREETINGS_LIST, greetings)
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import ReplyKeyboardMarkup, UpdateObj
from bot.views import create_goal_from_tg, get_goal_categories, get_goal_category, goals_list_4_tg
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError

from todolist.settings import TG_TOKEN


class Command(BaseCommand):
    help = "TG Bot to set and maintain goals"

    def get_tg_user(self, user_id: int) -> TgUser:
        try:
            tg_user = TgUser.objects.get(chat_id=user_id)

        except ObjectDoesNotExist:
            tg_user = TgUser(chat_id=user_id)
            tg_user.save()

        return tg_user

    def get_auth_code(self, tg_user: TgUser) -> int:
        """
        Генерирует код аутентификации и сохраняет его в  
        БД для связи с пользователем сервиса
        """
        auth_code = randint(100000, 999999)
        tg_user.verification_code = str(auth_code)
        tg_user.save()

        return auth_code

    def print_categories(self, tg_user: TgUser):
        categoryes = get_goal_categories(tg_user)
        # TODO: ВЫВОД КНОПОК В ТГ-БОТЕ + кнопка ОТМЕНЫ
        keyboard = self.tg_client.create_keyboard(categoryes, "ОТМЕНИТЬ")
        self.tg_client.send_message(tg_user.chat_id,
                                    "Выбери категорию",
                                    reply_markup=keyboard)

    def upd_handler(self, upd_objects: list[UpdateObj]) -> int:
        offset = 0

        for upd_obj in upd_objects:
            offset = upd_obj.update_id + 1

            # Можно удалить. Печатает в консоль полученное сообщение
            # от пользователя. Нужно ли оно мне сейчас?
            print(upd_obj.message)

            # Если есть аттрибут "ТЕКСТ" то обновление нас интересует
            if hasattr(upd_obj.message, 'text'):
                message = str(upd_obj.message.text)
                chat_id = upd_obj.message.chat.id

                self.message_handler(message, chat_id)

        return offset

    def message_handler(self, message: str, chat_id: int):
        # Сначала проверим состояние бота для этого юзера
        tg_user = self.get_tg_user(chat_id)
        state = tg_user.state

        if state == TgUser.State.not_confirmed:
            if not tg_user.verification_code:
                # Приветствие только тому кто написал впервые
                # И еще вообще не имеет записи в БД
                msg_to_user = greetings(GREETINGS_LIST)
                self.tg_client.send_message(chat_id, msg_to_user)

            auth_code = self.get_auth_code(tg_user)
            self.tg_client.send_message(chat_id, CODE_DESCRIPTION)
            self.tg_client.send_message(chat_id, f'ТВОЙ КОД: {auth_code}')

        elif state == TgUser.State.confirmed:
            if message == '/goals':
                goals_list = goals_list_4_tg(tg_user)
                self.tg_client.send_message(chat_id, goals_list)

            elif message == '/create':
                self.print_categories(tg_user)
                tg_user.state = TgUser.State.create_1
                tg_user.save()

            else:
                self.tg_client.send_message(chat_id, BAD_COMMAND)

        elif state == TgUser.State.create_1:
            categoryes = get_goal_categories(tg_user)

            if message in categoryes:
                category = get_goal_category(tg_user, message)
                tg_user.state = TgUser.State.create_2
                # Не могу придумать лучшего места для хранения выбранной
                # пользователем категории для создания цели...
                tg_user.create_goal_category = category
                tg_user.save()

                keyboard = self.tg_client.create_keyboard(["ОТМЕНИТЬ"])
                resp = self.tg_client.send_message(chat_id,
                                                   CREATE_2,
                                                   reply_markup=keyboard)

            elif message in ['ОТМЕНИТЬ', 'exit', 'cansel']:
                tg_user.state = TgUser.State.confirmed
                tg_user.save()

                # "Пустая" клавиатура, чтобы удалить текущую
                keyboard = self.tg_client.create_keyboard()
                resp = self.tg_client.send_message(chat_id,
                                                   CREATE_BRAKE,
                                                   reply_markup=keyboard)
                print(resp)

            else:
                self.tg_client.send_message(chat_id, BAD_CATEGORY)
                self.print_categories(tg_user)

        elif state == TgUser.State.create_2:
            # "Пустая" клавиатура, чтобы удалить текущую
            keyboard = self.tg_client.create_keyboard()

            if message in ['ОТМЕНИТЬ', 'exit', 'cansel']:
                resp = self.tg_client.send_message(chat_id,
                                                   CREATE_BRAKE,
                                                   reply_markup=keyboard)

            else:
                # Ну типа всё, тут создали наконец цель
                create_goal_from_tg(tg_user, message)
                self.tg_client.send_message(chat_id, CREATE_SUCCESS,
                                            reply_markup=keyboard)

            tg_user.state = TgUser.State.confirmed
            tg_user.create_goal_category = None
            tg_user.save()

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('БОТ ЗАПУЩЕН!'))
        offset = 0
        polling = True
        self.tg_client = TgClient(TG_TOKEN)

        while polling:
            # Проверка обновлений
            response = self.tg_client.get_updates(offset=offset)

            # Обработка обновлений
            offset = self.upd_handler(response.result)

        self.stdout.write(self.style.SUCCESS('БОТ ВЫКЛЮЧЕН'))
