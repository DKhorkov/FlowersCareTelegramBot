from typing import Type
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from v_2.configs import watering_intervals
from v_2.sql_alchemy.models import FlowersGroup


class BaseMarkupCreator:

    @staticmethod
    def base_markup() -> InlineKeyboardMarkup:
        base_markup = InlineKeyboardMarkup(row_width=1)
        add_group = InlineKeyboardButton(text='Добавить сценарий полива', callback_data='add_group')
        add_flower = InlineKeyboardButton(text='Добавить растение', callback_data='add_flower')
        check_groups = InlineKeyboardButton(text='Управление сценариями полива', callback_data='check_groups')
        check_flowers = InlineKeyboardButton(text='Управление растениями', callback_data='check_flowers')
        base_markup.add(add_group, add_flower, check_groups, check_flowers)
        return base_markup


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
        menu = InlineKeyboardButton(text='В меню 🏠', callback_data='group_adding_description MENU')
        add_group_description_markup.add(back_button, menu)
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
        menu = InlineKeyboardButton(text='В меню 🏠', callback_data='group_adding_interval MENU')
        add_group_watering_interval_markup.add(menu)
        return add_group_watering_interval_markup

    @staticmethod
    def back_to_menu_markup() -> InlineKeyboardMarkup:
        back_to_menu_markup = InlineKeyboardMarkup(row_width=1)
        menu = InlineKeyboardButton(text='В меню 🏠', callback_data='MENU')
        back_to_menu_markup.add(menu)
        return back_to_menu_markup


class AddFlowerMarkupCreator(BaseMarkupCreator):

    @staticmethod
    def add_flower_title_markup() -> InlineKeyboardMarkup:
        add_flower_title_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='flower_adding_title BACK')
        add_flower_title_markup.add(back_button)
        return add_flower_title_markup

    @staticmethod
    def add_flower_description_markup() -> InlineKeyboardMarkup:
        add_flower_description_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='flower_adding_description BACK')
        menu = InlineKeyboardButton(text='В меню 🏠', callback_data='flower_adding_description MENU')
        add_flower_description_markup.add(back_button, menu)
        return add_flower_description_markup

    @staticmethod
    def add_flower_group_markup(flowers_groups: list[Type[FlowersGroup]]) -> InlineKeyboardMarkup:
        add_flower_group_markup = InlineKeyboardMarkup(row_width=1)
        if len(flowers_groups) == 0:
            add_group_button = InlineKeyboardButton(
                text='Добавить сценарий полива',
                callback_data='flower_adding_group add_group'
            )

            add_flower_group_markup.add(add_group_button)

        for group in flowers_groups:
            group_button = InlineKeyboardButton(
                text=f'{group.title}',
                callback_data=f'flower_adding_group {group.title} {group.id}'
            )

            add_flower_group_markup.add(group_button)

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='flower_adding_group BACK')
        menu = InlineKeyboardButton(text='В меню 🏠', callback_data='flower_adding_group MENU')
        add_flower_group_markup.add(back_button, menu)
        return add_flower_group_markup

    @staticmethod
    def add_flower_photo_markup():
        add_flower_photo_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='flower_adding_photo BACK')
        menu = InlineKeyboardButton(text='В меню 🏠', callback_data='flower_adding_photo MENU')
        add_flower_photo_markup.add(back_button, menu)
        return add_flower_photo_markup

class MarkupCreator(AddGroupMarkupCreator, AddFlowerMarkupCreator):
    pass
