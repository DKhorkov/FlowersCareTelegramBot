from typing import Type
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from v_2.helpers.markup_creators.base_markup_creator import BaseMarkupCreator
from v_2.helpers.sql_alchemy.models import FlowersGroup


class AddFlowerMarkupCreator(BaseMarkupCreator):

    @staticmethod
    def add_flower_no_groups_markup() -> InlineKeyboardMarkup:
        add_flower_description_markup = InlineKeyboardMarkup(row_width=1)
        add_group_button = InlineKeyboardButton(
            text='Добавить сценарий полива',
            callback_data='flower_adding_no_groups add_group'
        )

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='flower_adding_no_groups BACK')
        add_flower_description_markup.add(add_group_button, back_button)
        return add_flower_description_markup

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
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='flower_adding_description MENU')
        add_flower_description_markup.add(back_button, menu_button)
        return add_flower_description_markup

    @staticmethod
    def add_flower_group_markup(flowers_groups: list[Type[FlowersGroup]]) -> InlineKeyboardMarkup:
        add_flower_group_markup = InlineKeyboardMarkup(row_width=1)
        for group in flowers_groups:
            group_button = InlineKeyboardButton(
                text=f'{group.title}',
                callback_data=f'flower_adding_group {group.id}'
            )
            add_flower_group_markup.add(group_button)

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='flower_adding_group BACK')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='flower_adding_group MENU')
        add_flower_group_markup.add(back_button, menu_button)
        return add_flower_group_markup

    @staticmethod
    def add_flower_ask_photo_markup():
        add_flower_ask_photo_markup = InlineKeyboardMarkup(row_width=1)
        yes_button = InlineKeyboardButton(text='Да', callback_data='flower_adding_ask_photo yes')
        no_button = InlineKeyboardButton(text='Нет', callback_data='flower_adding_ask_photo no')
        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='flower_adding_ask_photo BACK')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='flower_adding_ask_photo MENU')
        add_flower_ask_photo_markup.add(yes_button, no_button, back_button, menu_button)
        return add_flower_ask_photo_markup

    @staticmethod
    def add_flower_photo_markup():
        add_flower_photo_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='flower_adding_photo BACK')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='flower_adding_photo MENU')
        add_flower_photo_markup.add(back_button, menu_button)
        return add_flower_photo_markup

    @staticmethod
    def add_flower_created_markup() -> InlineKeyboardMarkup:
        add_flower_created_markup = InlineKeyboardMarkup(row_width=1)
        another_flower_button = InlineKeyboardButton(
            text='Добавить еще одно растение',
            callback_data='flower_adding_created another'
        )
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='flower_adding_created MENU')
        add_flower_created_markup.add(another_flower_button, menu_button)
        return add_flower_created_markup
