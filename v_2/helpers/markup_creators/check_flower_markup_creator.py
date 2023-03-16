from typing import Type
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from v_2.helpers.markup_creators.base_markup_creator import BaseMarkupCreator
from v_2.helpers.sql_alchemy.models import Flower, FlowersGroup


class CheckFlowerMarkupCreator(BaseMarkupCreator):

    @staticmethod
    def check_flower_selection_markup(user_flowers: list[Type[Flower]]) -> InlineKeyboardMarkup:
        check_flower_selection_markup = InlineKeyboardMarkup(row_width=1)
        if len(user_flowers) == 0:
            add_flower_button = InlineKeyboardButton(
                text='Добавить растение',
                callback_data='check_flower_selection add_flower'
            )

            check_flower_selection_markup.add(add_flower_button)

        for flower in user_flowers:
            flower_button = InlineKeyboardButton(
                text=f'{flower.title}',
                callback_data=f'check_flower_selection {flower.title} {flower.id}'
            )

            check_flower_selection_markup.add(flower_button)

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='check_flower_selection BACK')
        check_flower_selection_markup.add(back_button)
        return check_flower_selection_markup

    @staticmethod
    def check_flower_action_markup(flower_id: int) -> InlineKeyboardMarkup:
        check_flower_action_markup = InlineKeyboardMarkup(row_width=1)
        change_button = InlineKeyboardButton(
            text='Редактировать растение',
            callback_data=f'check_flower_action change {flower_id}'
        )

        delete_button = InlineKeyboardButton(
            text='Удалить растение',
            callback_data=f'check_flower_action delete {flower_id}'
        )

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data=f'check_flower_action BACK {flower_id}')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data=f'check_flower_action MENU {flower_id}')
        check_flower_action_markup.add(change_button, delete_button, back_button, menu_button)
        return check_flower_action_markup

    @staticmethod
    def check_flower_confirm_delete_markup(flower_id: int) -> InlineKeyboardMarkup:
        check_flower_confirm_delete_markup = InlineKeyboardMarkup(row_width=1)
        yes_button = InlineKeyboardButton(
            text='Подтвердить удаление',
            callback_data=f'check_flower_confirm_delete YES {flower_id}'
        )

        no_button = InlineKeyboardButton(
            text='Отменить удаление',
            callback_data=f'check_flower_confirm_delete NO {flower_id}'
        )

        menu_button = InlineKeyboardButton(
            text='В меню 🏠',
            callback_data=f'check_flower_confirm_delete MENU {flower_id}'
        )

        check_flower_confirm_delete_markup.add(yes_button, no_button, menu_button)
        return check_flower_confirm_delete_markup

    @staticmethod
    def check_flower_choose_changing_point_markup(flower_id: int) -> InlineKeyboardMarkup:
        check_flower_choose_changing_point_markup = InlineKeyboardMarkup(row_width=1)
        change_title_button = InlineKeyboardButton(
            text='Изменить название растения',
            callback_data=f'check_flower_choose_changing_point title {flower_id}'
        )

        change_description_button = InlineKeyboardButton(
            text='Изменить заметки по растению',
            callback_data=f'check_flower_choose_changing_point description {flower_id}'
        )

        change_photo_button = InlineKeyboardButton(
            text='Изменить фотографию растения',
            callback_data=f'check_flower_choose_changing_point photo {flower_id}'
        )

        change_group_button = InlineKeyboardButton(
            text='Изменить сценарий полива растения',
            callback_data=f'check_flower_choose_changing_point group {flower_id}'
        )

        back_button = InlineKeyboardButton(
            text='Назад ↩️',
            callback_data=f'check_flower_choose_changing_point BACK {flower_id}'
        )

        menu_button = InlineKeyboardButton(
            text='В меню 🏠',
            callback_data=f'check_flower_choose_changing_point MENU {flower_id}'
        )

        check_flower_choose_changing_point_markup.add(
            change_title_button, change_description_button, change_photo_button, change_group_button, back_button,
            menu_button)

        return check_flower_choose_changing_point_markup

    @staticmethod
    def check_flower_change_markup(flower_id: int) -> InlineKeyboardMarkup:
        check_flower_change_title_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data=f'check_flower_change BACK {flower_id}')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data=f'check_flower_change MENU {flower_id}')
        check_flower_change_title_markup.add(back_button, menu_button)
        return check_flower_change_title_markup

    @staticmethod
    def check_flower_change_group_markup(flower_id: int, user_groups: list[Type[FlowersGroup]]) -> InlineKeyboardMarkup:
        check_flower_change_group_markup = InlineKeyboardMarkup(row_width=1)
        for group in user_groups:
            group_button = InlineKeyboardButton(
                text=f'{group.title}',
                callback_data=f'check_flower_change_group {group.title} {group.id}'
            )

            check_flower_change_group_markup.add(group_button)

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data=f'check_flower_change_group BACK {flower_id}')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data=f'check_flower_change_group MENU {flower_id}')
        check_flower_change_group_markup.add(back_button, menu_button)
        return check_flower_change_group_markup
