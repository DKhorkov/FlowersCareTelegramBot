import pickle
import telebot

from typing import Type
from datetime import datetime
from telebot.types import InputMediaPhoto, Message
from telebot_calendar import CallbackData, RUSSIAN_LANGUAGE

from v_2.helpers.template_creator import TemplateCreator
from v_2.helpers.markup_creator import MarkupCreator
from v_2.helpers.logging_system import get_logger
from v_2.helpers.customized_calendar import CustomizedCalendar
from v_2.helpers.database_parser import DatabaseParser
from v_2.sql_alchemy.adapter import SQLAlchemyAdapter
from v_2.sql_alchemy.models import FlowersGroup, Flower


logger = get_logger('bot_logs')

calendar = CustomizedCalendar(language=RUSSIAN_LANGUAGE)
create_group_calendar_callback = CallbackData("create_group_calendar", "action", "year", "month", "day")
change_group_calendar_callback = CallbackData("change_group_calendar", "action", "year", "month", "day")


class StartMessageHandler:

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
                        media=open('static/images/media_message_picture.png', 'rb'),
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
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator.base_template(),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)


class AddGroupMessageHandler(StartMessageHandler):

    @staticmethod
    def send_add_group_title_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator.add_group_title_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator.add_group_title(),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_add_group_description_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().add_group_description_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_group_description(
                        json=json,
                        str_user_id=str(user_id)
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_add_group_watering_interval_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().add_group_watering_interval_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_group_watering_interval(
                        json=json,
                        str_user_id=str(user_id)
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_add_group_last_watering_date_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            now = datetime.now()

            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=calendar.create_calendar(
                    name=create_group_calendar_callback.prefix,
                    year=now.year,
                    month=now.month
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_group_watering_last_time(
                        json=json,
                        str_user_id=str(user_id)
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_add_group_created_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().add_group_created_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().group_created(
                        json=json,
                        str_user_id=str(user_id)
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)


class AddFlowerMessageHandler(StartMessageHandler):

    @staticmethod
    def send_add_flower_title_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().add_flower_title_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_flower_title(),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_add_flower_description_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().add_flower_description_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_flower_description(
                        json=json,
                        str_user_id=str(user_id)
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_add_flower_ask_photo_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().add_flower_ask_photo_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_flower_ask_photo(
                        json=json,
                        str_user_id=str(user_id)
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_add_flower_group_message(bot: telebot.TeleBot, user_id: int, json: dict,
                                      flowers_groups:  list[Type[FlowersGroup]]) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().add_flower_group_markup(
                    flowers_groups=flowers_groups
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_flower_group(
                        json=json,
                        str_user_id=str(user_id),
                        empty_groups=True if len(flowers_groups) > 0 else False
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_add_flower_photo_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().add_flower_photo_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_flower_photo(
                        json=json,
                        str_user_id=str(user_id)
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_add_flower_created_message(bot: telebot.TeleBot, user_id: int, json: dict, bytes_photo: bytes) -> None:
        try:
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

        except Exception as e:
            logger.error(e)


class CheckFlowerMessageHandler(StartMessageHandler):

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
                    media=open('static/images/media_message_picture.png', 'rb'),
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


class CheckGroupMessageHandler(StartMessageHandler):

    @staticmethod
    def send_check_group_selection_message(bot: telebot.TeleBot, user_id: int, json: dict,
                                           user_groups:  list[Type[FlowersGroup]]) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().check_group_selection_markup(
                    user_groups=user_groups
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_selection(
                        empty_groups=True if len(user_groups) > 0 else False
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_group_action_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                        group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().check_group_action_markup(
                    group_id=group_id
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_action(
                        group_description=DatabaseParser.parse_group(
                            sql_alchemy_adapter=sql_alchemy,
                            group=group
                        )
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_group_choose_changing_point_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                                       group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                    group_id=group_id
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_choose_changing_point(
                        group_description=DatabaseParser.parse_group(
                            sql_alchemy_adapter=sql_alchemy,
                            group=group
                        )
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_group_confirm_delete_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                                group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().check_group_confirm_delete_markup(
                    group_id=group_id
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_confirm_delete(
                        group_description=DatabaseParser.parse_group(
                            sql_alchemy_adapter=sql_alchemy,
                            group=group
                        )
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_group_see_flowers_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                             group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter,
                                             group_flowers: list[Type[Flower]]) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().check_group_see_flowers_markup(
                    group_flowers=group_flowers,
                    group_id=group_id
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_see_flowers(
                        group_description=DatabaseParser.parse_group(
                            sql_alchemy_adapter=sql_alchemy,
                            group=group
                        )
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_group_change_title_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                              group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().check_group_change_markup(
                    group_id=group_id
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_change_title(
                        group_description=DatabaseParser.parse_group(
                            sql_alchemy_adapter=sql_alchemy,
                            group=group
                        )
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_group_change_description_message(bot: telebot.TeleBot, user_id: int, json: dict, group_id: int,
                                                    group: Type[FlowersGroup], sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().check_group_change_markup(
                    group_id=group_id
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_change_description(
                        group_description=DatabaseParser.parse_group(
                            sql_alchemy_adapter=sql_alchemy,
                            group=group
                        )
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_group_change_last_watering_date_message(bot: telebot.TeleBot, json: dict, group: Type[FlowersGroup],
                                                           user_id: int, sql_alchemy: SQLAlchemyAdapter) -> None:
        try:
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
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_change_last_watering_date(
                        group_description=DatabaseParser.parse_group(
                            sql_alchemy_adapter=sql_alchemy,
                            group=group
                        )
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)

    @staticmethod
    def send_check_group_change_watering_interval_message(bot: telebot.TeleBot, json: dict, group: Type[FlowersGroup],
                                                          user_id: int, sql_alchemy: SQLAlchemyAdapter,
                                                          group_id: int) -> None:
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=json[str(user_id)]['message_for_update'],
                reply_markup=MarkupCreator().check_group_change_watering_interval_markup(
                    group_id=group_id
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_change_watering_interval(
                        group_description=DatabaseParser.parse_group(
                            sql_alchemy_adapter=sql_alchemy,
                            group=group
                        )
                    ),
                    parse_mode='HTML'
                )
            )

        except Exception as e:
            logger.error(e)


class MessageHandler(AddGroupMessageHandler, AddFlowerMessageHandler, CheckFlowerMessageHandler,
                     CheckGroupMessageHandler):
    pass
