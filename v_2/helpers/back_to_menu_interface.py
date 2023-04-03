import pickle

import telebot

from v_2.helpers.message_handlers.main_message_handler import MessageHandler
from v_2.helpers.sql_alchemy.adapter import SQLAlchemyAdapter


class BackToMenuInterface:

    def call_place_spreader(self, bot: telebot.TeleBot, user_id: int, json: dict, call_place: str,
                            sql_alchemy: SQLAlchemyAdapter, adding_photo: bool) -> None:
        match call_place:
            case 'group_description':
                self.__back_to_group_description(bot=bot, user_id=user_id, json=json)
            case 'group_last_watering_date':
                self.__back_to_group_last_watering_date(bot=bot, user_id=user_id, json=json)
            case 'group_watering_interval':
                self.__back_to_group_watering_interval(bot=bot, user_id=user_id, json=json)
            case 'group_confirm_data':
                self.__back_to_group_confirm_data(bot=bot, user_id=user_id, json=json)
            case 'flower_description':
                self.__back_to_flower_description(bot=bot, user_id=user_id, json=json)
            case 'flower_group':
                self.__back_to_flower_group(bot=bot, user_id=user_id, json=json, sql_alchemy=sql_alchemy)
            case 'flower_ask_photo':
                self.__back_to_flower_ask_photo(bot=bot, user_id=user_id, json=json)
            case 'flower_photo':
                self.__back_to_flower_photo(bot=bot, user_id=user_id, json=json)
            case 'flower_confirm_data':
                self.__back_to_flower_confirm_data(bot=bot, user_id=user_id, json=json, adding_photo=adding_photo)

    @staticmethod
    def __back_to_group_description(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        MessageHandler.send_add_group_description_message(bot=bot, user_id=user_id, json=json)

    @staticmethod
    def __back_to_group_last_watering_date(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        MessageHandler.send_add_group_last_watering_date_message(bot=bot, user_id=user_id, json=json)

    @staticmethod
    def __back_to_group_watering_interval(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        MessageHandler.send_add_group_watering_interval_message(bot=bot, user_id=user_id, json=json)

    @staticmethod
    def __back_to_group_confirm_data(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        MessageHandler.send_add_group_confirm_data_message(bot=bot, user_id=user_id, json=json)

    @staticmethod
    def __back_to_flower_description(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        MessageHandler.send_add_flower_description_message(bot=bot, user_id=user_id, json=json)

    @staticmethod
    def __back_to_flower_group(bot: telebot.TeleBot, user_id: int, json: dict, sql_alchemy: SQLAlchemyAdapter) -> None:
        MessageHandler.send_add_flower_group_message(
            bot=bot,
            user_id=user_id,
            json=json,
            flowers_groups=sql_alchemy.get_user_groups(user_id)
        )

    @staticmethod
    def __back_to_flower_ask_photo(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        MessageHandler.send_add_flower_ask_photo_message(bot=bot, user_id=user_id, json=json)

    @staticmethod
    def __back_to_flower_photo(bot: telebot.TeleBot, user_id: int, json: dict) -> None:
        MessageHandler.send_add_flower_photo_message(bot=bot, user_id=user_id, json=json)

    @staticmethod
    def __back_to_flower_confirm_data(bot: telebot.TeleBot, user_id: int, json: dict, adding_photo: bool) -> None:
        if adding_photo:
            with open(f'users_photos/{user_id}/flower_photo.png', 'rb') as photo_file:
                bytes_photo = pickle.dumps(photo_file.read())
        else:
            with open('helpers/static/images/base_flower_picture.png', 'rb') as photo_file:
                bytes_photo = pickle.dumps(photo_file.read())

        MessageHandler.send_add_flower_confirm_data_message(
            bot=bot,
            user_id=user_id,
            json=json,
            bytes_photo=bytes_photo,
            adding_photo=adding_photo
        )
