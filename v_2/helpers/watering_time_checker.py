import logging
import time

import telebot

from typing import Type
from datetime import datetime
from telebot.types import Message

from v_2.helpers.sql_alchemy.models import User, FlowersGroup, Flower
from v_2.helpers.sql_alchemy.adapter import SQLAlchemyAdapter
from v_2.helpers.message_handlers.main_message_handler import MessageHandler
from v_2.configs import push_notification_interval


class WateringTimeChecker:

    def __init__(self, bot: telebot.TeleBot, sql_alchemy: SQLAlchemyAdapter, logger: logging.Logger) -> None:
        self.__bot = bot
        self.__alchemy = sql_alchemy
        self.__logger = logger

    def check_subscribes(self) -> None:
        while True:
            try:
                groups = self.__alchemy.get_all_groups()
                for group in groups:
                    current_time = datetime.now()
                    next_watering_time = datetime.strptime(group.next_watering_date, '%Y-%m-%d %H:%M:%S')
                    if  next_watering_time < current_time:
                        user = self.__alchemy.get_user_by_id(group.user_id)
                        group_flowers = self.__alchemy.get_group_flowers(group_id=group.id)
                        self.__send_notification(user, group, group_flowers)
            except Exception as e:
                self.__logger.info(e)

            time.sleep(push_notification_interval)

    def __send_notification(self, user: Type[User], group: Type[FlowersGroup],
                            group_flowers: list[Type[Flower]]) -> None:
        today = str(datetime.today()).split(" ")[0]
        current_date = datetime.strptime(today + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        notification_message = MessageHandler.send_watering_notification_message(
            bot=self.__bot,
            user_id=user.user_id,
            group_flowers=group_flowers,
            group=group,
            current_date=current_date
        )

        self.__update_group_notification(
            group=group,
            notification_message=notification_message,
            user=user
        )

    def __update_group_notification(self, group: Type[FlowersGroup], notification_message: Message,
                                    user: Type[User]) -> None:
        exists = self.__alchemy.check_group_notification_existence(group_id=group.id)
        if not exists:
            self.__alchemy.add_notification(group_id=group.id, message_id=notification_message.id)
        else:
            notification = self.__alchemy.get_notification(group_id=group.id)
            MessageHandler.delete_notification_message(
                bot=self.__bot,
                user_id=user.user_id,
                message_id=notification.message_id
            )

            self.__alchemy.change_notification_message_id(group_id=group.id, message_id=notification_message.id)
