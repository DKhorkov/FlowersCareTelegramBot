import telebot

from telebot.types import InputMediaPhoto, Message

from v_2.helpers.template_creators.main_template_creator import TemplateCreator
from v_2.helpers.markup_creators.main_markup_creator import MarkupCreator
from v_2.helpers.logging_system import get_logger

logger = get_logger('bot_logs')


class BaseMessageHandler:

    @staticmethod
    def delete_message(bot: telebot.TeleBot, message: Message) -> None:
        try:
            bot.delete_message(chat_id=message.from_user.id, message_id=message.id)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_start_message(bot: telebot.TeleBot, message: Message) -> int | None:
        try:
            message_to_update = bot.send_media_group(
                chat_id=message.from_user.id,
                media=[
                    InputMediaPhoto(
                        media=open('helpers/static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator.base_template(),
                        parse_mode='HTML'
                    )
                ]
            )[0].id

            bot.edit_message_reply_markup(
                chat_id=message.from_user.id,
                message_id=message_to_update,
                reply_markup=MarkupCreator.base_markup()
            )

            bot.delete_message(
                chat_id=message.from_user.id,
                message_id=message.id
            )

            return message_to_update
        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_back_to_menu_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator.base_markup(),
                media=InputMediaPhoto(
                    media=open('helpers/static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator.base_template(),
                    parse_mode='HTML'
                )
            )
        except Exception as e:
            logger.error(e)
