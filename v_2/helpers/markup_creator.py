from typing import Type
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from v_2.configs import watering_intervals
from v_2.sql_alchemy.models import FlowersGroup, Flower


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

    @staticmethod
    def back_to_menu_markup() -> InlineKeyboardMarkup:
        back_to_menu_markup = InlineKeyboardMarkup(row_width=1)
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='MENU')
        back_to_menu_markup.add(menu_button)
        return back_to_menu_markup


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
    def add_group_created_markup() -> InlineKeyboardMarkup:
        add_flower_created_markup = InlineKeyboardMarkup(row_width=1)
        add_flower_button = InlineKeyboardButton(
            text='Добавить растение',
            callback_data='group_adding_created add_flower'
        )

        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='group_adding_created MENU')
        add_flower_created_markup.add(add_flower_button, menu_button)
        return add_flower_created_markup


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


class CheckGroupMarkupCreator(BaseMarkupCreator):

    @staticmethod
    def check_group_selection_markup(user_groups: list[Type[FlowersGroup]]) -> InlineKeyboardMarkup:
        check_group_selection_markup = InlineKeyboardMarkup(row_width=1)
        if len(user_groups) == 0:
            add_flower_button = InlineKeyboardButton(
                text='Добавить сценарий полива растений',
                callback_data='check_group_selection add_group'
            )

            check_group_selection_markup.add(add_flower_button)

        for group in user_groups:
            group_button = InlineKeyboardButton(
                text=f'{group.title}',
                callback_data=f'check_group_selection {group.title} {group.id}'
            )

            check_group_selection_markup.add(group_button)

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='check_group_selection BACK')
        check_group_selection_markup.add(back_button)
        return check_group_selection_markup

    @staticmethod
    def check_group_action_markup(group_id: int) -> InlineKeyboardMarkup:
        check_group_action_markup = InlineKeyboardMarkup(row_width=1)
        change_button = InlineKeyboardButton(
            text='Редактировать сценарий полива',
            callback_data=f'check_group_action change {group_id}'
        )

        delete_button = InlineKeyboardButton(
            text='Удалить сценарий полива',
            callback_data=f'check_group_action delete {group_id}'
        )

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data=f'check_group_action BACK {group_id}')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data=f'check_group_action MENU {group_id}')
        check_group_action_markup.add(change_button, delete_button, back_button, menu_button)
        return check_group_action_markup

    @staticmethod
    def check_group_confirm_delete_markup(group_id: int) -> InlineKeyboardMarkup:
        check_group_confirm_delete_markup = InlineKeyboardMarkup(row_width=1)
        yes_button = InlineKeyboardButton(
            text='Подтвердить удаление',
            callback_data=f'check_group_confirm_delete YES {group_id}'
        )

        no_button = InlineKeyboardButton(
            text='Отменить удаление',
            callback_data=f'check_group_confirm_delete NO {group_id}'
        )

        menu_button = InlineKeyboardButton(
            text='В меню 🏠',
            callback_data=f'check_group_confirm_delete MENU {group_id}'
        )

        check_group_confirm_delete_markup.add(yes_button, no_button, menu_button)
        return check_group_confirm_delete_markup


class MarkupCreator(AddGroupMarkupCreator, AddFlowerMarkupCreator, CheckFlowerMarkupCreator, CheckGroupMarkupCreator):
    pass
