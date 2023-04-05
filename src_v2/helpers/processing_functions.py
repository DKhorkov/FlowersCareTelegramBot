from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from src_v2.helpers.json_handler import JsonHandler
from src_v2.helpers.message_handlers.main_message_handler import MessageHandler
from src_v2.helpers.sql_alchemy.adapter import SQLAlchemyAdapter
from src_v2.configs import json_name


def get_user_groups_and_flowers(sql_alchemy: SQLAlchemyAdapter, user_id: int) -> tuple[list, list]:
    user_groups = sql_alchemy.get_user_groups(user_id)
    user_flowers = sql_alchemy.get_user_flowers(user_id)
    return user_groups, user_flowers

def change_group_title(bot: TeleBot, message: Message, sql_alchemy: SQLAlchemyAdapter) -> None:
    group_id, group_title, json = JsonHandler(json_name).deactivate_refactor_group_title(message)

    sql_alchemy.change_group_title(
        group_id=group_id,
        new_title=group_title
    )

    MessageHandler.delete_message(bot=bot, user_id=message.from_user.id, message_id=message.id)
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

    MessageHandler.delete_message(bot=bot, user_id=message.from_user.id, message_id=message.id)
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

    MessageHandler.delete_message(bot=bot, user_id=message.from_user.id, message_id=message.id)
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

    MessageHandler.delete_message(bot=bot, user_id=message.from_user.id, message_id=message.id)
    MessageHandler.send_check_flower_choose_changing_point_message(
        bot=bot,
        user_id=message.from_user.id,
        json=json,
        flower=sql_alchemy.get_flower(flower_id),
        flower_id=flower_id,
        sql_alchemy=sql_alchemy
    )


def add_or_update_message_for_update(bot: TeleBot, message: Message | CallbackQuery,
                                     sql_alchemy: SQLAlchemyAdapter) -> None:
    message_for_update = JsonHandler(json_name).get_user_message_for_update(message.from_user.id)
    if message_for_update is not None:
        MessageHandler.delete_message(bot=bot, user_id=message.from_user.id, message_id=message_for_update)

    user_groups, user_flowers = get_user_groups_and_flowers(sql_alchemy=sql_alchemy, user_id=message.from_user.id)
    message_for_update = MessageHandler().send_start_message(
        bot=bot,
        message=message,
        user_flowers=user_flowers,
        user_groups=user_groups
    )
    JsonHandler(json_name).prepare_json(user_id=message.from_user.id, message_for_update=message_for_update)
