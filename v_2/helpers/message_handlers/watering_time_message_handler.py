import telebot

from datetime import datetime, timedelta
from typing import Type

from v_2.helpers.template_creators.main_template_creator import TemplateCreator
from v_2.helpers.markup_creators.main_markup_creator import MarkupCreator
from v_2.helpers.logging_system import get_logger
from v_2.helpers.message_handlers.base_message_handler import BaseMessageHandler
from v_2.helpers.sql_alchemy.models import Flower, FlowersGroup


logger = get_logger('bot_logs')


class WateringTimeMessageHandler(BaseMessageHandler):

    @staticmethod
    def send_watering_notification_message(bot: telebot.TeleBot, user_id: int, group: Type[FlowersGroup],
                                           group_flowers: list[Type[Flower]], current_date: datetime) -> None:
        try:
            watering_notification_message_id = bot.send_message(
                chat_id=user_id,
                reply_markup=MarkupCreator().group_watering_status_markup(group_id=group.id, current_date=current_date),
                text=TemplateCreator().group_watering_status(group=group, group_flowers=group_flowers),
                parse_mode='HTML'
                ).id

        except Exception as e:
            logger.error(e)