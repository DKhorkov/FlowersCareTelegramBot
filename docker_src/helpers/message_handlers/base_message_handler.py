import os
import telebot

from telebot.types import InputMediaPhoto, Message
from telebot.apihelper import ApiTelegramException

from . .template_creators.main_template_creator import TemplateCreator
from . .markup_creators.main_markup_creator import MarkupCreator
from . .logging_system import get_logger
from . .photo_paths_handler import PhotoPathsHandler


logger = get_logger('bot_logs')


class BaseMessageHandler:

    @staticmethod
    def delete_message(bot: telebot.TeleBot, user_id: int, message_id: int) -> None:
        try:
            bot.delete_message(chat_id=user_id, message_id=message_id)
        except ApiTelegramException:
            pass
        except Exception as e:
            logger.error(f'{e} Failed to delete message from user_id={user_id} and message_id={message_id}!')

    def send_start_message(self, bot: telebot.TeleBot, message: Message, user_flowers: list,
                           user_groups: list) -> int | None:
        message_id_to_update = bot.send_media_group(
            chat_id=message.from_user.id,
            media=[
                InputMediaPhoto(
                    media=open(os.path.join(os.getcwd(), PhotoPathsHandler.start_picture.value), 'rb'),
                    caption=TemplateCreator.base_template(),
                    parse_mode='HTML'
                )
            ]
        )[0].id

        bot.edit_message_reply_markup(
            chat_id=message.from_user.id,
            message_id=message_id_to_update,
            reply_markup=MarkupCreator.base_markup(user_groups=user_groups, user_flowers=user_flowers)
        )

        self.delete_message(bot=bot, user_id=message.from_user.id, message_id=message.id)
        return message_id_to_update
