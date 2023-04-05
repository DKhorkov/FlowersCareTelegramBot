from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

class BaseMarkupCreator:

    @staticmethod
    def base_markup(user_groups: list, user_flowers: list) -> InlineKeyboardMarkup:
        base_markup = InlineKeyboardMarkup(row_width=1)
        add_group = InlineKeyboardButton(text='Добавить сценарий полива', callback_data='add_group')
        base_markup.add(add_group)

        if len(user_groups) != 0:
            add_flower = InlineKeyboardButton(text='Добавить растение', callback_data='add_flower')
            check_groups = InlineKeyboardButton(text='Управление сценариями полива', callback_data='check_groups')
            base_markup.add(add_flower, check_groups)

        if len(user_flowers) != 0:
            check_flowers = InlineKeyboardButton(text='Управление растениями', callback_data='check_flowers')
            base_markup.add(check_flowers)

        return base_markup
