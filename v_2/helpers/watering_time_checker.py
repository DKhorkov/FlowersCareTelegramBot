import logging
import telebot

from typing import Type
from datetime import datetime


from v_2.helpers.sql_alchemy.models import User, FlowersGroup, Flower
from v_2.helpers.sql_alchemy.adapter import SQLAlchemyAdapter
from v_2.helpers.message_handlers.main_message_handler import MessageHandler
from v_2.configs import TOKEN


class WateringTimeChecker:

    def __init__(self, bot: telebot.TeleBot, sql_alchemy: SQLAlchemyAdapter):
        self.__bot = bot
        self.__alchemy = sql_alchemy

    def check_subscribes(self):
        groups = self.__alchemy.get_all_groups()
        for group in groups:
            current_time = datetime.now()
            next_wateting_time = datetime.strptime(group.next_watering_date, '%Y-%m-%d %H:%M:%S')
            if  next_wateting_time < current_time:
                user = self.__alchemy.get_user_by_id(group.user_id)
                group_flowers = self.__alchemy.get_group_flowers(group_id=group.id)
                self.__send_notification(user, group, group_flowers)

    def __send_notification(self, user: Type[User], group: Type[FlowersGroup], group_flowers: list[Type[Flower]]):
        today = str(datetime.today()).split(" ")[0]
        current_date = datetime.strptime(today + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        MessageHandler.send_watering_notification_message(
            bot=self.__bot,
            user_id=user.user_id,
            group_flowers=group_flowers,
            group=group,
            current_date=current_date
        )


if __name__ == '__main__':
    wtc = WateringTimeChecker(telebot.TeleBot(token=TOKEN),
                              SQLAlchemyAdapter(logger=logging.getLogger(""), path_to_db='../sqlite_tg_bot_db.db'))
    wtc.check_subscribes()