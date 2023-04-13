import os
import telebot

from datetime import datetime
from typing import Type
from telebot.types import InputMediaPhoto
from telebot_calendar import CallbackData, RUSSIAN_LANGUAGE

from src_v2.helpers.customized_calendar import CustomizedCalendar
from src_v2.helpers.template_creators.main_template_creator import TemplateCreator
from src_v2.helpers.markup_creators.main_markup_creator import MarkupCreator
from src_v2.helpers.logging_system import get_logger
from src_v2.helpers.message_handlers.base_message_handler import BaseMessageHandler
from src_v2.helpers.sql_alchemy.models import Flower, FlowersGroup
from src_v2.helpers.sql_alchemy.adapter import SQLAlchemyAdapter
from src_v2.helpers.database_parser import DatabaseParser
from src_v2.helpers.photo_paths_handler import PhotoPathsHandler


logger = get_logger('bot_logs')

calendar = CustomizedCalendar(language=RUSSIAN_LANGUAGE)
create_group_calendar_callback = CallbackData("create_group_calendar", "action", "year", "month", "day")
change_group_calendar_callback = CallbackData("change_group_calendar", "action", "year", "month", "day")


class CheckGroupMessageHandler(BaseMessageHandler):

    @staticmethod
    def send_check_group_selection_message(bot: telebot.TeleBot, user_id: int, json: dict,
                                           user_groups:  list[Type[FlowersGroup]]) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_group_selection_markup(
                user_groups=user_groups
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.media_message_picture.value), 'rb'),
                caption=TemplateCreator().check_group_selection(
                    empty_groups=True if len(user_groups) > 0 else False
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_group_action_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                        group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_group_action_markup(
                group_id=group_id
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.media_message_picture.value), 'rb'),
                caption=TemplateCreator().check_group_action(
                    group_description=DatabaseParser().parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_group_confirm_delete_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                                group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_group_confirm_delete_markup(
                group_id=group_id
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.media_message_picture.value), 'rb'),
                caption=TemplateCreator().check_group_confirm_delete(
                    group_description=DatabaseParser().parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_group_choose_changing_point_message(bot: telebot.TeleBot, group: Type[FlowersGroup], user_id: int,
                                                       json: dict, group_id: int,sql_alchemy: SQLAlchemyAdapter
                                                       ) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                group_id=group_id
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.media_message_picture.value), 'rb'),
                caption=TemplateCreator().check_group_choose_changing_point(
                    group_description=DatabaseParser().parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_group_see_flowers_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                             group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter,
                                             group_flowers: list[Type[Flower]]) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_group_see_flowers_markup(
                group_flowers=group_flowers,
                group_id=group_id
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.media_message_picture.value), 'rb'),
                caption=TemplateCreator().check_group_see_flowers(
                    group_flowers_length=len(group_flowers),
                    group_description=DatabaseParser().parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_group_change_title_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                              group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_group_change_markup(
                group_id=group_id
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.group_title_picture.value), 'rb'),
                caption=TemplateCreator().check_group_change_title(
                    group_description=DatabaseParser().parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_group_change_description_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                                    group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_group_change_markup(
                group_id=group_id
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.group_description_picture.value), 'rb'),
                caption=TemplateCreator().check_group_change_description(
                    group_description=DatabaseParser().parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_group_change_last_watering_date_message(bot: telebot.TeleBot, json: dict, group: Type[FlowersGroup],
                                                           user_id: int, sql_alchemy: SQLAlchemyAdapter) -> None:
        now = datetime.now()
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=calendar.create_calendar(
                name=change_group_calendar_callback.prefix,
                year=now.year,
                month=now.month
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.group_last_watering_date_picture.value), 'rb'),
                caption=TemplateCreator().check_group_change_last_watering_date(
                    group_description=DatabaseParser().parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_check_group_change_watering_interval_message(bot: telebot.TeleBot, json: dict, group: Type[FlowersGroup],
                                                          user_id: int, sql_alchemy: SQLAlchemyAdapter,
                                                          group_id: int) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().check_group_change_watering_interval_markup(
                group_id=group_id
            ),
            media=InputMediaPhoto(
                media=open(os.path.join(os.getcwd(), PhotoPathsHandler.group_watering_interval_picture.value), 'rb'),
                caption=TemplateCreator().check_group_change_watering_interval(
                    group_description=DatabaseParser().parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )
