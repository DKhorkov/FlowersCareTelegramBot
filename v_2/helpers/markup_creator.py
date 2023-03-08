from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from v_2.configs import watering_intervals


class MarkupCreator:

    @staticmethod
    def base_markup():
        base_markup = InlineKeyboardMarkup(row_width=1)
        add_group = InlineKeyboardButton('Создать сценарий полива', callback_data='add_group')
        add_flower = InlineKeyboardButton('Добавить цветок', callback_data='add_flower')
        check_groups = InlineKeyboardButton('Управление сценариями полива', callback_data='check_groups')
        check_flowers = InlineKeyboardButton('Управление цветками', callback_data='check_flowers')
        base_markup.add(add_group, add_flower, check_groups, check_flowers)
        return base_markup

    @staticmethod
    def add_group_name_markup():
        add_group_name_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton('Назад ↩️', callback_data='group_adding_name BACK')
        add_group_name_markup.add(back_button)
        return add_group_name_markup

    @staticmethod
    def add_group_description_markup():
        add_group_description_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton('Назад ↩️', callback_data='group_adding_description BACK')
        menu = InlineKeyboardButton('В меню 🏠', callback_data='group_adding_description MENU')
        add_group_description_markup.add(back_button, menu)
        return add_group_description_markup

    @staticmethod
    def add_group_watering_interval_markup():
        add_group_watering_interval_markup = InlineKeyboardMarkup(row_width=2)
        interval_buttons_list = []
        for num in watering_intervals:
            if num in [1, 21]:
                interval_button = InlineKeyboardButton(f'{num} день', callback_data=f'group_adding_interval {num}')
            elif num in [2, 3, 4]:
                interval_button = InlineKeyboardButton(f'{num} дня', callback_data=f'group_adding_interval {num}')
            else:
                interval_button = InlineKeyboardButton(f'{num} дней', callback_data=f'group_adding_interval {num}')

            interval_buttons_list.append(interval_button)

        add_group_watering_interval_markup.add(*interval_buttons_list)

        back_button = InlineKeyboardButton('Назад ↩️', callback_data='group_adding_interval BACK')
        add_group_watering_interval_markup.add(back_button)
        menu = InlineKeyboardButton('В меню 🏠', callback_data='group_adding_interval MENU')
        add_group_watering_interval_markup.add(menu)
        return add_group_watering_interval_markup

    @staticmethod
    def back_to_menu_markup():
        back_to_menu_markup = InlineKeyboardMarkup(row_width=1)
        menu = InlineKeyboardButton( 'В меню 🏠', callback_data='MENU')
        back_to_menu_markup.add(menu)
        return back_to_menu_markup


