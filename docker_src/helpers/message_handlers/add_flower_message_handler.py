import os
import telebot
import pickle

from typing import Type
from telebot.types import InputMediaPhoto

from . .template_creators.main_template_creator import TemplateCreator
from . .markup_creators.main_markup_creator import MarkupCreator
from . .logging_system import get_logger
from .base_message_handler import BaseMessageHandler
from . .sql_alchemy.models import FlowersGroup
from . .photo_paths_handler import PhotoPathsHandler


logger = get_logger('bot_logs')


class AddFlowerMessageHandler(BaseMessageHandler):

    @staticmethod
    def send_add_flower_title_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_flower_title_markup(),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.add_flower_title_picture.value), 'rb'),
                caption=TemplateCreator().add_flower_title(),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_flower_description_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_flower_description_markup(),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.add_flower_description_picture.value), 'rb'),
                caption=TemplateCreator().add_flower_description(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_flower_group_message(bot: telebot.TeleBot, user_id: int, json: dict,
                                      flowers_groups:  list[Type[FlowersGroup]]) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_flower_group_markup(
                flowers_groups=flowers_groups
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.add_flower_group_picture.value), 'rb'),
                caption=TemplateCreator().add_flower_group(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_flower_ask_photo_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_flower_ask_photo_markup(),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.add_flower_photo_picture.value), 'rb'),
                caption=TemplateCreator().add_flower_ask_photo(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_flower_photo_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_flower_photo_markup(),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.add_flower_photo_picture.value), 'rb'),
                caption=TemplateCreator().add_flower_photo(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_flower_confirm_data_message(bot: telebot.TeleBot, user_id: int, json: dict,
                                             bytes_photo: bytes, adding_photo: bool) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_flower_confirm_data_markup(adding_photo=adding_photo),
            media=InputMediaPhoto(
                media=pickle.loads(bytes_photo),
                caption=TemplateCreator().add_flower_confirm_data(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_flower_created_message(bot: telebot.TeleBot, user_id: int, json: dict, bytes_photo: bytes) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_flower_created_markup(),
            media=InputMediaPhoto(
                media=pickle.loads(bytes_photo),
                caption=TemplateCreator().flower_created(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )
