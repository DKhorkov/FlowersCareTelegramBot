from typing import Type

from v_2.sql_alchemy.models import FlowersGroup, Flower
from v_2.sql_alchemy.adapter import SQLAlchemyAdapter


class DatabaseParser:

    @staticmethod
    def parse_flower(sql_alchemy_adapter: SQLAlchemyAdapter, flower: Type[Flower]) -> str:
        flowers_group = sql_alchemy_adapter.get_flowers_group(flower.group_id)
        return f"<b>Название растения:</b> {flower.title}\n" \
               f"<b>Заметки по растению:</b> {flower.description}\n" \
               f"<b>Сценарий полива:</b> {flowers_group.title}\n\n"
