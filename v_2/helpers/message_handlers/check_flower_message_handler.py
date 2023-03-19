import telebot
import pickle

from typing import Type
from telebot.types import InputMediaPhoto

from v_2.helpers.template_creators.main_template_creator import TemplateCreator
from v_2.helpers.markup_creators.main_markup_creator import MarkupCreator
from v_2.helpers.logging_system import get_logger
from v_2.helpers.message_handlers.base_message_handler import BaseMessageHandler
from v_2.helpers.sql_alchemy.models import Flower, FlowersGroup
from v_2.helpers.sql_alchemy.adapter import SQLAlchemyAdapter
from v_2.helpers.database_parser import DatabaseParser


logger = get_logger('bot_logs')


class CheckFlowerMessageHandler(BaseMessageHandler):

    @staticmethod
    def send_check_flower_selection_message(bot: telebot.TeleBot, user_id: int, json: dict,
                                            user_flowers:  list[Type[Flower]]) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().check_flower_selection_markup(
                    user_flowers=user_flowers
                ),
                media=InputMediaPhoto(
                    media=open('helpers/static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_flower_selection(
                        empty_flowers=True if len(user_flowers) > 0 else False
                    ),
                    parse_mode='HTML'
                )
            )
        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_flower_action_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                         flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
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
        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_flower_change_title_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                               flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
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
        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_flower_change_description_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                                     flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
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
        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_flower_change_photo_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                               flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
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
        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_flower_change_group_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                               flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter,
                                               user_groups: list[Type[FlowersGroup]]) -> None:
        try:
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
        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_flower_choose_changing_point_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                                        flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
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
        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_flower_confirm_delete_message(bot: telebot.TeleBot, user_id: int, json: dict, flower_id: int,
                                                 flower: Type[Flower], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
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
        except Exception as e:
            logger.error(e)