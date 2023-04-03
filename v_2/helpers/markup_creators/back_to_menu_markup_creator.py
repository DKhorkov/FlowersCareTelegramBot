from typing import Type
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from v_2.helpers.markup_creators.base_markup_creator import BaseMarkupCreator
from v_2.helpers.sql_alchemy.models import FlowersGroup, Flower
from v_2.configs import watering_intervals


class BackToMenuMarkupCreator(BaseMarkupCreator):

    @staticmethod
    def confirm_back_to_menu_markup(call_place: str, adding_photo: bool) -> InlineKeyboardMarkup:
        confirm_back_to_menu_markup = InlineKeyboardMarkup(row_width=1)
        yes_button = InlineKeyboardButton(
            text='Да, хочу выйти в меню🤠',
            callback_data='back_to_menu YES'
        )

        no_button = InlineKeyboardButton(
            text='Нет, только не мои данные😱',
            callback_data=f'back_to_menu NO {adding_photo} {call_place}'
        )

        confirm_back_to_menu_markup.add(yes_button, no_button)
        return confirm_back_to_menu_markup

    @staticmethod
    def back_to_menu_markup() -> InlineKeyboardMarkup:
        back_to_menu_markup = InlineKeyboardMarkup(row_width=1)
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='MENU')
        back_to_menu_markup.add(menu_button)
        return back_to_menu_markup