from typing import ClassVar, Type
# from dataclasses import dataclass
from typing import Optional
from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    id: int
    type: str  # "private", "group", "supergroup", or "channel"
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    message_id: int
    user: Optional[User]
    date: int
    chat: Chat
    text: Optional[str]

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Optional[Message]

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: list[UpdateObj]  # todo
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Optional[Message]  # todo
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class KeyboardButton:
    text: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class ReplyKeyboardMarkup:
    keyboard: list[list[KeyboardButton]]
    is_persistent: bool = False
    resize_keyboard: bool = True
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class ReplyKeyboardRemove:
    remove_keyboard: bool = True
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
