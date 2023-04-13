import os
import telebot
import pickle

from typing import Type
from telebot.types import InputMediaPhoto

from . .template_creators.main_template_creator import TemplateCreator
from . .markup_creators.main_markup_creator import MarkupCreator
from . .logging_system import get_logger
from .base_message_handler import BaseMessageHandler
from . .sql_alchemy.models import Flower, FlowersGroup
from . .sql_alchemy.adapter import SQLAlchemyAdapter
from . .database_parser import DatabaseParser
from . .photo_paths_handler import PhotoPathsHandler


logger = get_logger('bot_logs')


class CheckFlowerMessageHandler(BaseMessageHandler):

    @staticmethod
    def send_check_flower_selection_message(bot: telebot.TeleBot, user_id: int, json: dict,
                                            user_flowers:  list[Type[Flower]]) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_selection_markup(
                user_flowers=user_flowers
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.media_message_picture.value), 'rb'),
                caption=TemplateCreator().check_flower_selection(
                    empty_flowers=True if len(user_flowers) > 0 else False
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_flower_action_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                         flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_action_markup(
                flower_id=flower_id
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_action(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_flower_confirm_delete_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                                 flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_confirm_delete_markup(
                flower_id=flower_id
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_confirm_delete(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_flower_choose_changing_point_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                                        flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_choose_changing_point_markup(
                flower_id=flower_id
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_choose_changing_point(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_flower_change_title_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                               flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_change_markup(
                flower_id=flower_id
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_change_title(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_flower_change_description_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                                     flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_change_markup(
                flower_id=flower_id
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_change_description(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_flower_change_photo_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                               flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_change_markup(
                flower_id=flower_id
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_change_photo(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_flower_change_group_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                               flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter,
                                               user_groups: list[Type[FlowersGroup]]) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_change_group_markup(
                flower_id=flower_id,
                user_groups=user_groups
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_change_group(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
                ),
                parse_mode='HTML'
            )
        )
