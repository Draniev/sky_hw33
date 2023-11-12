import requests
from bot.tg.dc import (GetUpdatesResponse, KeyboardButton, ReplyKeyboardMarkup,
                       ReplyKeyboardRemove, SendMessageResponse)


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url('getUpdates')
        response = requests.get(url=f'{url}?offset={offset}&timeout={timeout}')
        return GetUpdatesResponse.Schema().load(response.json())

    def send_message(self, chat_id: int, text: str, **kwargs) -> SendMessageResponse:
        url = self.get_url('sendMessage')
        data = {
            'chat_id': chat_id,
            'text': text,
        }

        # Так можно добавить любой нужный параметр в объект отправки сообщения,
        # Например, клавиатуру (см. спецификацию тг)
        for key, value in kwargs.items():
            data[key] = value

        response = requests.post(url=url, json=data)
        # response = requests.get(url=f'{url}?chat_id={chat_id}&text={text}')
        return SendMessageResponse.Schema().load(response.json())

    def create_keyboard(self, keys: list[str] = [], *args):
        """
        keys: Список кнопок, которы добавить. Просто текстовый списо
        если список пустой, то клавиатура будет УДАЛЕНА, сама она не уходит
        Надо сказать, реализация с т.з. архитектуры, вероятно, ужасна, тут бы
        какой то приличный конструктор, наверное... ну да ладно, так сойдет =)
        """
        if len(keys):
            buttons = [[KeyboardButton(key)] for key in keys]
            for item in args:
                buttons.append([KeyboardButton(item)])

            reply_keyboard = ReplyKeyboardMarkup(buttons)
            return ReplyKeyboardMarkup.Schema().dump(reply_keyboard)

        else:
            reply_keyboard = ReplyKeyboardRemove()
            return ReplyKeyboardRemove.Schema().dump(reply_keyboard)
