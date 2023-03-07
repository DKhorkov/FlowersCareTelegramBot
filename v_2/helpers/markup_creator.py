from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


class MarkupCreator:

    @staticmethod
    def create_base_markup():
        base_markup = InlineKeyboardMarkup(row_width=1)
        add_group = InlineKeyboardButton('Создать группу', callback_data='add_group')
        add_flower = InlineKeyboardButton('Добавить цветок', callback_data='add_flower')
        check_groups = InlineKeyboardButton('Управление группами', callback_data='check_groups')
        check_flowers = InlineKeyboardButton('Управление цветками', callback_data='check_flowers')
        base_markup.add(add_group, add_flower, check_groups, check_flowers)
        return base_markup

    @staticmethod
    def create_add_group_name_markup():
        set_group_name_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton('Назад ↩️', callback_data='group_adding_name BACK')
        set_group_name_markup.add(back_button)
        return set_group_name_markup

    @staticmethod
    def create_add_group_description_markup():
        set_group_description_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton('Назад ↩️', callback_data='group_adding_description BACK')
        menu = InlineKeyboardButton('В меню 🏠', callback_data='group_adding_description MENU')
        set_group_description_markup.add(back_button, menu)
        return set_group_description_markup

