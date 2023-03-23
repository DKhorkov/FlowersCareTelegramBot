from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

class BaseMarkupCreator:

    @staticmethod
    def base_markup(user_groups: list, user_flowers: list) -> InlineKeyboardMarkup:
        base_markup = InlineKeyboardMarkup(row_width=1)
        add_group = InlineKeyboardButton(text='Добавить сценарий полива', callback_data='add_group')
        add_flower = InlineKeyboardButton(text='Добавить растение', callback_data='add_flower')
        base_markup.add(add_group, add_flower)

        if len(user_groups) != 0:
            check_groups = InlineKeyboardButton(text='Управление сценариями полива', callback_data='check_groups')
            base_markup.add(check_groups)

        if len(user_flowers) != 0:
            check_flowers = InlineKeyboardButton(text='Управление растениями', callback_data='check_flowers')
            base_markup.add(check_flowers)

        return base_markup

    @staticmethod
    def back_to_menu_markup() -> InlineKeyboardMarkup:
        back_to_menu_markup = InlineKeyboardMarkup(row_width=1)
        menu_button = InlineKeyboardButton(text='В меню 🏠', callback_data='MENU')
        back_to_menu_markup.add(menu_button)
        return back_to_menu_markup
