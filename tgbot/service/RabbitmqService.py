import json

from asyncio import ProactorEventLoop

from tgbot.core.ConversationModel import ConversationModel
from tgbot.core.RabbitmqTgbot import RabbitmqTgbot
from tgbot.handlers.conversation_handler import send_message_to_user


class RabbitmqService:
    @classmethod
    def send_data_rabbitmq(cls, user_id: int, message_type: str, text_data: str = ""):
        chat = ConversationModel().get_chat_info(user_id)

        request = (json.dumps(
            {
                "type": message_type,
                "user_id": chat.id,
                "lang": chat.lang.name,
                "theme": chat.theme.name,
                "lvl": chat.lvl.name,
                "text": text_data,
                "answer": ""
            }))

        RabbitmqTgbot().send(request)

    @classmethod
    def send_message(cls, data: json, loop: ProactorEventLoop = None):
        data = json.loads(data)

        send_message_to_user(data["user_id"], data["answer"], loop)