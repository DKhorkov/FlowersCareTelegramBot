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
    def create_group_adding_markup():
        group_adding_markup = InlineKeyboardMarkup(row_width=1)
        back_button = InlineKeyboardButton('Назад ↩️', callback_data=f'group_adding_name BACK')
        group_adding_markup.add(back_button)
        return group_adding_markup

