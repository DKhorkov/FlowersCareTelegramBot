from typing import Type
from datetime import datetime

from v_2.helpers.sql_alchemy.models import FlowersGroup, Flower
from v_2.helpers.sql_alchemy.adapter import SQLAlchemyAdapter


class DatabaseParser:

    @staticmethod
    def parse_flower(sql_alchemy_adapter: SQLAlchemyAdapter, flower: Type[Flower]) -> str:
        flowers_group = sql_alchemy_adapter.get_group(flower.group_id)
        return f"<b>Название растения:</b> {flower.title}\n" \
               f"<b>Заметки по растению:</b> {flower.description}\n" \
               f"<b>Сценарий полива:</b> {flowers_group.title}\n\n"

    def parse_group(self, sql_alchemy_adapter: SQLAlchemyAdapter, group: Type[FlowersGroup]) -> str:
        number_of_flowers = sql_alchemy_adapter.get_number_of_flowers_in_group(group.id)
        if group.watering_interval in [1, 21]:
            days = 'день'
        elif group.watering_interval in [2, 3, 4]:
            days = 'дня'
        else:
            days = 'дней'

        return f"<b>Название сценария полива:</b> {group.title}\n" \
               f"<b>Описание сценария полива:</b> {group.description}\n" \
               f"<b>Количество растений в сценарии:</b> {number_of_flowers}\n\n" \
               f"<b>Дата последнего полива:</b> {self._transform_to_russian_date(group.last_watering_date)}\n" \
               f"<b>Интервал полива:</b> {group.watering_interval} {days}\n" \
               f"<b>Дата следующего полива:</b> {self._transform_to_russian_date(group.next_watering_date)}\n\n"

    @staticmethod
    def _transform_to_russian_date(str_date: str) -> str:
        datetime_date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
        processed_date = datetime.strftime(datetime_date, '%d-%m-%Y')
        return processed_date
