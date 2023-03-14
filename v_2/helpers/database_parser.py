from typing import Type

from v_2.sql_alchemy.models import FlowersGroup, Flower
from v_2.sql_alchemy.adapter import SQLAlchemyAdapter


class DatabaseParser:

    @staticmethod
    def parse_flower(sql_alchemy_adapter: SQLAlchemyAdapter, flower: Type[Flower]) -> str:
        flowers_group = sql_alchemy_adapter.get_group(flower.group_id)
        return f"<b>Название растения:</b> {flower.title}\n" \
               f"<b>Заметки по растению:</b> {flower.description}\n" \
               f"<b>Сценарий полива:</b> {flowers_group.title}\n\n"

    @staticmethod
    def parse_group(sql_alchemy_adapter: SQLAlchemyAdapter, group: Type[FlowersGroup]) -> str:
        number_of_flowers = sql_alchemy_adapter.get_number_of_flowers_in_group(group.id)
        return f"<b>Название сценария полива:</b> {group.title}\n" \
               f"<b>Описание сценария полива:</b> {group.description}\n" \
               f"<b>Количество растений в сценарии:</b> {number_of_flowers}\n\n" \
               f"<b>Дата последнего полива:</b> {group.last_watering_date.split(' ')[0]}\n" \
               f"<b>Интервал полива:</b> {group.watering_interval}\n" \
               f"<b>Дата следующего полива:</b> {group.next_watering_date.split(' ')[0]}\n\n"
