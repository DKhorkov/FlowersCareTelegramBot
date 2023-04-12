import telebot

from datetime import datetime
from telebot.types import InputMediaPhoto
from telebot_calendar import CallbackData, RUSSIAN_LANGUAGE

from . .template_creators.main_template_creator import TemplateCreator
from . .markup_creators.main_markup_creator import MarkupCreator
from . .logging_system import get_logger
from . .customized_calendar import CustomizedCalendar
from .base_message_handler import BaseMessageHandler


logger = get_logger('bot_logs')

calendar = CustomizedCalendar(language=RUSSIAN_LANGUAGE)
create_group_calendar_callback = CallbackData("create_group_calendar", "action", "year", "month", "day")
change_group_calendar_callback = CallbackData("change_group_calendar", "action", "year", "month", "day")


class AddGroupMessageHandler(BaseMessageHandler):

    @staticmethod
    def send_add_group_title_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator.add_group_title_markup(),
            media=InputMediaPhoto(
                media=open('helpers/static/images/group_title_picture.png', 'rb'),
                caption=TemplateCreator.add_group_title(),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_group_description_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_group_description_markup(),
            media=InputMediaPhoto(
                media=open('helpers/static/images/group_description_picture.png', 'rb'),
                caption=TemplateCreator().add_group_description(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_group_last_watering_date_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
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
                media=open('helpers/static/images/group_last_watering_date_picture.png', 'rb'),
                caption=TemplateCreator().add_group_watering_last_time(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_group_watering_interval_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_group_watering_interval_markup(),
            media=InputMediaPhoto(
                media=open('helpers/static/images/group_watering_interval_picture.png', 'rb'),
                caption=TemplateCreator().add_group_watering_interval(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_group_confirm_data_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_group_confirm_data_markup(),
            media=InputMediaPhoto(
                media=open('helpers/static/images/add_group_confirm_data_picture.png', 'rb'),
                caption=TemplateCreator().add_group_confirm_data(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )

    @staticmethod
    def send_add_group_created_message(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        bot.edit_message_media(
            chat_id=user_id,
            message_id=json[str(user_id)]['message_for_update'],
            reply_markup=MarkupCreator().add_group_created_markup(),
            media=InputMediaPhoto(
                media=open('helpers/static/images/add_group_created_picture.png', 'rb'),
                caption=TemplateCreator().group_created(
                    json=json,
                    str_user_id=str(user_id)
                ),
                parse_mode='HTML'
            )
        )
