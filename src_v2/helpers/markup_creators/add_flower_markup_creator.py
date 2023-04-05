from typing import Type
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from src_v2.helpers.markup_creators.base_markup_creator import BaseMarkupCreator
from src_v2.helpers.sql_alchemy.models import FlowersGroup


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
    def add_flower_confirm_data_markup(adding_photo: bool) -> InlineKeyboardMarkup:
        add_flower_confirm_data_markup = InlineKeyboardMarkup(row_width=1)
        confirm_button = InlineKeyboardButton(
            text='Все верно ✅',
            callback_data=f'flower_adding_confirm_data confirm_flower_data {adding_photo}'
        )

        back_button = InlineKeyboardButton(
            text='Назад ↩️',
            callback_data=f'flower_adding_confirm_data BACK {adding_photo}'
        )

        menu_button = InlineKeyboardButton(
            text='В меню 🏠',
            callback_data=f'flower_adding_confirm_data MENU {adding_photo}'
        )

        add_flower_confirm_data_markup.add(confirm_button, back_button, menu_button)
        return add_flower_confirm_data_markup

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
