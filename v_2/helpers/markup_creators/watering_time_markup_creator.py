from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

from v_2.helpers.markup_creators.base_markup_creator import BaseMarkupCreator


class WateringTimeMarkupCreator(BaseMarkupCreator):

    @staticmethod
    def group_watering_status_markup(group_id: int, current_date: datetime):
        group_watering_status_markup = InlineKeyboardMarkup(row_width=1)
        group_watered = InlineKeyboardButton(
            text='Растения в данном сценарии политы ✅',
            callback_data=f'group_watering_status YES {current_date} {group_id}'
        )

        group_not_watered = InlineKeyboardButton(
            text='Растения в данном сценарии НЕ политы ❌',
            callback_data=f'group_watering_status NO {current_date} {group_id}'
        )

        group_watering_status_markup.add(group_watered, group_not_watered)
        return group_watering_status_markup
