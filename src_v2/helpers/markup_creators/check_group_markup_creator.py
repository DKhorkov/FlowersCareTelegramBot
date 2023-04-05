from typing import Type
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from src_v2.helpers.markup_creators.base_markup_creator import BaseMarkupCreator
from src_v2.helpers.sql_alchemy.models import FlowersGroup, Flower
from src_v2.configs import watering_intervals


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
                callback_data=f'check_group_selection {group.id}'
            )
            check_group_selection_markup.add(group_button)

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data='check_group_selection BACK')
        check_group_selection_markup.add(back_button)
        return check_group_selection_markup

    @staticmethod
    def check_group_action_markup(group_id: int) -> InlineKeyboardMarkup:
        check_group_action_markup = InlineKeyboardMarkup(row_width=1)
        see_flowers_button = InlineKeyboardButton(
            text='Просмотр растений в данном сценарии',
            callback_data=f'check_group_action see_flowers {group_id}'
        )

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
        check_group_action_markup.add(see_flowers_button, change_button, delete_button, back_button, menu_button)
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

    @staticmethod
    def check_group_choose_changing_point_markup(group_id: int) -> InlineKeyboardMarkup:
        check_group_choose_changing_point_markup = InlineKeyboardMarkup(row_width=1)
        change_title_button = InlineKeyboardButton(
            text='Изменить название',
            callback_data=f'check_group_choose_changing_point title {group_id}'
        )

        change_description_button = InlineKeyboardButton(
            text='Изменить описание',
            callback_data=f'check_group_choose_changing_point description {group_id}'
        )

        change_last_time_watering_button = InlineKeyboardButton(
            text='Изменить дату последнего полива',
            callback_data=f'check_group_choose_changing_point last_watering_date {group_id}'
        )

        change_watering_interval_button = InlineKeyboardButton(
            text='Изменить интервал полива',
            callback_data=f'check_group_choose_changing_point watering_interval {group_id}'
        )

        back_button = InlineKeyboardButton(
            text='Назад ↩️',
            callback_data=f'check_group_choose_changing_point BACK {group_id}'
        )

        menu_button = InlineKeyboardButton(
            text='В меню 🏠',
            callback_data=f'check_group_choose_changing_point MENU {group_id}'
        )

        check_group_choose_changing_point_markup.add(
            change_title_button, change_description_button, change_last_time_watering_button,
            change_watering_interval_button, back_button, menu_button)

        return check_group_choose_changing_point_markup

    @staticmethod
    def check_group_change_markup(group_id: int) -> InlineKeyboardMarkup:
        check_flower_change_title_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data=f'check_group_change BACK {group_id}')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data=f'check_group_change MENU {group_id}')
        check_flower_change_title_markup.add(back_button, menu_button)
        return check_flower_change_title_markup

    @staticmethod
    def check_group_change_watering_interval_markup(group_id: int) -> InlineKeyboardMarkup:
        check_group_change_watering_interval_markup = InlineKeyboardMarkup(row_width=2)
        interval_buttons_list = []
        for num in watering_intervals:
            if num in [1, 21]:
                interval_button = InlineKeyboardButton(
                    text=f'{num} день',
                    callback_data=f'check_group_change_watering_interval {num} {group_id}'
                )
            elif num in [2, 3, 4]:
                interval_button = InlineKeyboardButton(
                    text=f'{num} дня',
                    callback_data=f'check_group_change_watering_interval {num} {group_id}'
                )
            else:
                interval_button = InlineKeyboardButton(
                    text=f'{num} дней',
                    callback_data=f'check_group_change_watering_interval {num} {group_id}'
                )
            interval_buttons_list.append(interval_button)

        check_group_change_watering_interval_markup.add(*interval_buttons_list)

        back_button = InlineKeyboardButton(
            text='Назад ↩️',
            callback_data=f'check_group_change_watering_interval BACK {group_id}'
        )

        menu_button = InlineKeyboardButton(
            text='В меню 🏠',
            callback_data=f'check_group_change_watering_interval MENU {group_id}'
        )

        check_group_change_watering_interval_markup.add(back_button)
        check_group_change_watering_interval_markup.add(menu_button)
        return check_group_change_watering_interval_markup

    @staticmethod
    def check_group_see_flowers_markup(group_id: int, group_flowers: list[Type[Flower]]) -> InlineKeyboardMarkup:
        check_group_see_flowers_markup = InlineKeyboardMarkup(row_width=1)
        for flower in group_flowers:
            group_flower_button = InlineKeyboardButton(
                text=f'{flower.title}',
                callback_data=f'check_group_see_flowers {flower.id} {group_id}'
            )
            check_group_see_flowers_markup.add(group_flower_button)

        if len(group_flowers) == 0:
            add_flower_button = InlineKeyboardButton(
                text='Добавить растение',
                callback_data=f'check_group_see_flowers add_flower {group_id}'
            )
            check_group_see_flowers_markup.add(add_flower_button)

        back_button = InlineKeyboardButton(text='Назад ↩️', callback_data=f'check_group_see_flowers BACK {group_id}')
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data=f'check_group_see_flowers MENU {group_id}')
        check_group_see_flowers_markup.add(back_button, menu_button)
        return check_group_see_flowers_markup
