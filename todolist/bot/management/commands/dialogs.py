from random import randint


GREETINGS_LIST = [
    ("Привет! Похоже, мы с тобой еще не знакомы. Я бот-помошник, "
     "умею напоминать тебе про твои цели и помогать ставить новые. Но,"
     " чтобы нам с тобой начать работать, нужно познакомиться поближе."),
    ("Приветствую! Мы с тобой еще не знакомы? Чтобы продолжить общение"
     " нужно для начала обменяться кодами допуска."),
    ("Дарова! Нам бы, для начала, узнать друг-друга получше. У тебя ведь "
     "уже есть аккаунт в нашем сервисе по ведению целей? Если нет, то нужно"
     " зарегистрироваться."),
    ("Так, давай сразу к делу."),
]

CODE_DESCRIPTION = ("Для авторизации используй предоставленный мной токен. "
                    "Введи его на сайте в соответствующее поле в настройках"
                    " аккаунта.")
BAD_COMMAND = (
    "Вам доступны только следующие команды: "
    "\n/goals - показывает список текущих целей, "
    "\n/create - создаёт новую цель."
)


def greetings(greetings_list: list[str]) -> str:
    num = randint(0, len(greetings_list)-1)
    return greetings_list[num]
