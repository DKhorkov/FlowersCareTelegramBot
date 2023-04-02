from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from v_2.helpers.markup_creators.base_markup_creator import BaseMarkupCreator
from v_2.configs import watering_intervals


class AddGroupMarkupCreator(BaseMarkupCreator):

    @staticmethod
    def add_group_title_markup() -> InlineKeyboardMarkup:
        add_group_title_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='group_adding_title BACK')
        add_group_title_markup.add(back_button)
        return add_group_title_markup

    @staticmethod
    def add_group_description_markup() -> InlineKeyboardMarkup:
        add_group_description_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='group_adding_description BACK')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='group_adding_description MENU')
        add_group_description_markup.add(back_button, menu_button)
        return add_group_description_markup

    @staticmethod
    def add_group_watering_interval_markup() -> InlineKeyboardMarkup:
        add_group_watering_interval_markup = InlineKeyboardMarkup(row_width=2)
        interval_buttons_list = []
        for num in watering_intervals:
            if num in [1, 21]:
                interval_button = InlineKeyboardButton(text=f'{num} день', callback_data=f'group_adding_interval {num}')
            elif num in [2, 3, 4]:
                interval_button = InlineKeyboardButton(text=f'{num} дня', callback_data=f'group_adding_interval {num}')
            else:
                interval_button = InlineKeyboardButton(text=f'{num} дней', callback_data=f'group_adding_interval {num}')
            interval_buttons_list.append(interval_button)

        add_group_watering_interval_markup.add(*interval_buttons_list)

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='group_adding_interval BACK')
        add_group_watering_interval_markup.add(back_button)
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='group_adding_interval MENU')
        add_group_watering_interval_markup.add(menu_button)
        return add_group_watering_interval_markup

    @staticmethod
    def add_group_confirm_data_markup() -> InlineKeyboardMarkup:
        add_group_confirm_data_markup = InlineKeyboardMarkup(row_width=1)
        confirm_button = InlineKeyboardButton(
            text='Все верно ✅',
            callback_data='group_adding_confirm_data confirm_group_data'
        )

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='group_adding_confirm_data BACK')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='group_adding_confirm_data MENU')
        add_group_confirm_data_markup.add(confirm_button, back_button, menu_button)
        return add_group_confirm_data_markup
    @staticmethod
    def add_group_created_markup() -> InlineKeyboardMarkup:
        add_flower_created_markup = InlineKeyboardMarkup(row_width=1)
        add_flower_button = InlineKeyboardButton(
            text='Добавить растение',
            callback_data='group_adding_created add_flower'
        )
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='group_adding_created MENU')
        add_flower_created_markup.add(add_flower_button, menu_button)
        return add_flower_created_markup
