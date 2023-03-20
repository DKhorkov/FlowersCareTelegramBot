from telebot import TeleBot
from telebot.types import Message

from v_2.helpers.json_handler import JsonHandler
from v_2.helpers.message_handlers.main_message_handler import MessageHandler
from v_2.helpers.sql_alchemy.adapter import SQLAlchemyAdapter
from v_2.configs import json_name



def change_group_title(bot: TeleBot, message: Message, sql_alchemy: SQLAlchemyAdapter) -> None:
    group_id, group_title, json = JsonHandler(json_name).deactivate_refactor_group_title(message)

    sql_alchemy.change_group_title(
        group_id=group_id,
        new_title=group_title
    )

    MessageHandler.delete_message(bot=bot, message=message)
    MessageHandler.send_check_group_choose_changing_point_message(
        bot=bot,
        user_id=message.from_user.id,
        json=json,
        group_id=group_id,
        group=sql_alchemy.get_group(group_id),
        sql_alchemy=sql_alchemy
    )


def change_group_description(bot: TeleBot, message: Message, sql_alchemy: SQLAlchemyAdapter) -> None:
    group_id, group_description, json = JsonHandler(json_name).deactivate_refactor_group_description(message)

    sql_alchemy.change_group_description(
        group_id=group_id,
        new_description=group_description
    )

    MessageHandler.delete_message(bot=bot, message=message)
    MessageHandler.send_check_group_choose_changing_point_message(
        bot=bot,
        user_id=message.from_user.id,
        json=json,
        group_id=group_id,
        group=sql_alchemy.get_group(group_id),
        sql_alchemy=sql_alchemy
    )


def change_flower_title(bot: TeleBot, message: Message, sql_alchemy: SQLAlchemyAdapter) -> None:
    flower_id, flower_title, json = JsonHandler(json_name).deactivate_refactor_flower_title(message)

    sql_alchemy.change_flower_title(
        flower_id=flower_id,
        new_title=flower_title
    )

    MessageHandler.delete_message(bot=bot, message=message)
    MessageHandler.send_check_flower_choose_changing_point_message(
        bot=bot,
        user_id=message.from_user.id,
        json=json,
        flower=sql_alchemy.get_flower(flower_id),
        flower_id=flower_id,
        sql_alchemy=sql_alchemy
    )


def change_flower_description(bot: TeleBot, message: Message, sql_alchemy: SQLAlchemyAdapter) -> None:
    flower_id, flower_description, json = JsonHandler(json_name).deactivate_refactor_flower_description(message)

    sql_alchemy.change_flower_description(
        flower_id=flower_id,
        new_description=flower_description
    )

    MessageHandler.delete_message(bot=bot, message=message)
    MessageHandler.send_check_flower_choose_changing_point_message(
        bot=bot,
        user_id=message.from_user.id,
        json=json,
        flower=sql_alchemy.get_flower(flower_id),
        flower_id=flower_id,
        sql_alchemy=sql_alchemy
    )
