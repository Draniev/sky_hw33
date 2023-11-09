from random import randint
from typing import Tuple

from bot.management.commands.dialogs import (CODE_DESCRIPTION, GREETINGS_LIST,
                                             greetings, BAD_COMMAND)
from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import UpdateObj
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from bot.views import goals_list_4_tg

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
        auth_code = randint(100000, 999999)
        tg_user.verification_code = str(auth_code)
        tg_user.save()

        return auth_code

    def upd_handler(self, tg_client: TgClient,
                    upd_objects: list[UpdateObj]) -> int:
        offset = 0

        for upd_obj in upd_objects:
            offset = upd_obj.update_id + 1
            print(upd_obj.message)

            if hasattr(upd_obj.message, 'text'):
                message = str(upd_obj.message.text)
                chat_id = upd_obj.message.chat.id
                # tg_username = upd_obj.message.chat.username

                # Сначала проверим состояние бота для этого юзера
                tg_user = self.get_tg_user(chat_id)
                state = tg_user.state

                if state == TgUser.State.not_confirmed:
                    if not tg_user.verification_code:
                        msg_to_user = greetings(GREETINGS_LIST)
                        tg_client.send_message(chat_id, msg_to_user)

                    auth_code = self.get_auth_code(tg_user)
                    tg_client.send_message(chat_id, CODE_DESCRIPTION)
                    tg_client.send_message(chat_id, f'ТВОЙ КОД: {auth_code}')

                elif state == TgUser.State.confirmed:
                    if message == '/goals':
                        goals_list = goals_list_4_tg(tg_user)
                        tg_client.send_message(chat_id, goals_list)
                    elif message == '/create':
                        pass
                    else:
                        tg_client.send_message(chat_id, BAD_COMMAND)

                elif state == TgUser.State.create_1:
                    pass

                elif state == TgUser.State.create_2:
                    pass

                # if 'exit' in str(message):
                #     time_to_exit = True

        return offset

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('БОТ ЗАПУЩЕН!'))
        offset = 0
        polling = True
        tg_client = TgClient(TG_TOKEN)

        while polling:
            # Проверка обновлений
            response = tg_client.get_updates(offset=offset)

            # Вызываем выход ПОСЛЕ отправки запроса обновлений
            # Для подтверождения получения предыдущего
            # if time_to_exit:
            #     self.stdout.write(self.style.SUCCESS('Попали на выход'))
            #     polling = False

            offset = self.upd_handler(tg_client, response.result)

        self.stdout.write(self.style.SUCCESS('БОТ ВЫКЛЮЧЕН'))
