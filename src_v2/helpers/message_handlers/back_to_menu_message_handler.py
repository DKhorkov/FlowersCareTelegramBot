import os
import telebot

from telebot.types import InputMediaPhoto

from src_v2.helpers.template_creators.main_template_creator import TemplateCreator
from src_v2.helpers.markup_creators.main_markup_creator import MarkupCreator
from src_v2.helpers.logging_system import get_logger
from src_v2.helpers.message_handlers.base_message_handler import BaseMessageHandler
from src_v2.helpers.photo_paths_handler import PhotoPathsHandler


logger = get_logger('bot_logs')


class BackToMenuMessageHandler(BaseMessageHandler):

    CONFIRM_MESSAGE_TEXT = f'Уверен, что хочешь выйти в меню?\nВсе введенные данные будут удалены😔'

    @staticmethod
    def send_confirm_back_to_menu_message(bot: telebot.TeleBot, user_id: int, json: dict, call_place: str,
                                          adding_photo: bool = False) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator.confirm_back_to_menu_markup(call_place=call_place, adding_photo=adding_photo),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.start_picture.value), 'rb'),
                caption=BackToMenuMessageHandler.CONFIRM_MESSAGE_TEXT,
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_back_to_menu_message(bot: telebot.TeleBot, user_id: int, json: dict, user_groups: list,
                                  user_flowers: list) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator.base_markup(user_groups=user_groups, user_flowers=user_flowers),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.start_picture.value), 'rb'),
                caption=TemplateCreator.base_template(),
                parse_mode='HTML'
            )
        )