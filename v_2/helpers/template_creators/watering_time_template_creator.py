from typing import Type

from v_2.helpers.sql_alchemy.models import FlowersGroup, Flower
from v_2.helpers.template_creators.base_template_creator import BaseTemplateCreator


class WateringTimeTemplateCreator(BaseTemplateCreator):

    @staticmethod
    def group_watering_status(group: Type[FlowersGroup], group_flowers: list[Type[Flower]]) -> str:
        notification = f'Необходимо полить растения, принадлежащие к следующему сценарию полива: \n\n' \
                       f'<b>Название сценария:</b> {group.title}\n' \
                       f'<b>Описание сценария:</b> {group.description}\n' \
                       f'<b>Дата последнего полива сценария:</b> {group.last_watering_date.split(" ")[0]}\n' \
                       f'<b>Интервал полива сценария:</b> {group.watering_interval}\n\n' \
                       f'Растения в данном сценарии:\n'

        for numer, flower in enumerate(group_flowers, start=1):
            notification += f'{numer}) {flower.title}\n'

        notification += '\nРастения в данном сценарии были политы сегодня?'
        return notification