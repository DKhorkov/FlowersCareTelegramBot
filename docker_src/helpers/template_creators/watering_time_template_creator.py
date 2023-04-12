from typing import Type

from . .sql_alchemy.models import FlowersGroup, Flower
from .base_template_creator import BaseTemplateCreator


class WateringTimeTemplateCreator(BaseTemplateCreator):

    def group_watering_status(self, group: Type[FlowersGroup], group_flowers: list[Type[Flower]]) -> str:
        days = self.__get_watering_interval_days_name(watering_interval=group.watering_interval)
        notification = f'Необходимо полить растения, принадлежащие к следующему сценарию полива: \n\n' \
                       f'<b>Название сценария:</b> {group.title}\n' \
                       f'<b>Описание сценария:</b> {group.description}\n' \
                       f'<b>Дата последнего полива сценария:</b> ' \
                       f'{self._transform_to_russian_date(group.last_watering_date)}\n' \
                       f'<b>Интервал полива сценария:</b> {group.watering_interval} {days}\n\n' \
                       f'Растения в данном сценарии:\n'

        for numer, flower in enumerate(group_flowers, start=1):
            notification += f'{numer}) {flower.title}\n'

        if len(group_flowers) == 0:
            notification += 'В данный сценарий полива пока что не было добавлено ни одно растение!\n'

        notification += '\nРастения в данном сценарии были политы сегодня?'
        return notification

    @classmethod
    def __get_watering_interval_days_name(cls, watering_interval: int) -> str:
        if watering_interval in [1, 21]:
            days = 'день'
        elif watering_interval in [2, 3, 4]:
            days = 'дня'
        else:
            days = 'дней'

        return days
