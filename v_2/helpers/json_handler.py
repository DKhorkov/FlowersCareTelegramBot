import json
import os

from typing import Type
from telebot.types import Message
from datetime import datetime, timedelta

from v_2.helpers.sql_alchemy.models import FlowersGroup


class JsonHandler:

    def __init__(self, json_name: str) -> None:
        self.json_name = json_name

    def read_json_file(self) -> dict:
        if not os.path.exists('JSON_data'):
            os.mkdir('JSON_data')

        if not os.path.exists(f'JSON_data/{self.json_name}'):
            with open(f'JSON_data/{self.json_name}', 'w') as file:
                file.write(json.dumps({}))

        with open(f'JSON_data/{self.json_name}', 'r') as file:
            json_data = json.loads(file.read())

        return json_data

    def write_json_data(self, updated_json: dict) -> None:
        if not os.path.exists('JSON_data'):
            os.mkdir('JSON_data')

        with open(f'JSON_data/{self.json_name}', 'w') as file:
            file.write(json.dumps(updated_json))

    def prepare_json(self, user_id: int, message_for_update: int):
        str_user_id = str(user_id)
        json_data = self.read_json_file()
        json_data[str_user_id] = {}
        json_data[str_user_id]['message_for_update'] = message_for_update
        self.write_json_data(json_data)
        self.reset_appropriate_messages(user_id)

    def reset_appropriate_messages(self, user_id: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.read_json_file()
        json_data[str_user_id]['set_group_title'] = False
        json_data[str_user_id]['set_group_description'] = False
        json_data[str_user_id]['set_flower_title'] = False
        json_data[str_user_id]['set_flower_description'] = False
        json_data[str_user_id]['set_flower_photo'] = False
        json_data[str_user_id]['refactor'] = False
        self.write_json_data(json_data)
        return json_data

    def process_watering_interval(self, user_id: int, watering_interval: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.read_json_file()
        json_data[str_user_id]['watering_interval'] = watering_interval
        next_watering_date = datetime.strptime(
            json_data[str_user_id]['last_watering_date'],
            '%Y-%m-%d %H:%M:%S') + timedelta(days=watering_interval)
        json_data[str_user_id]['next_watering_date'] = str(next_watering_date)
        self.write_json_data(json_data)
        return json_data

    def activate_group_title(self, user_id: int) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['set_group_title'] = True
        self.write_json_data(json_data)
        return json_data

    def deactivate_group_title(self, user_id: int) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['set_group_title'] = False
        self.write_json_data(json_data)
        return json_data

    def activate_group_description(self, user_id: int) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['set_group_description'] = True
        self.write_json_data(json_data)
        return json_data

    def activate_group_description_and_write_title(self, message: Message) -> dict:
        str_user_id = str(message.from_user.id)
        json_data = self.read_json_file()
        json_data[str_user_id]['set_group_title'] = False
        json_data[str_user_id]['set_group_description'] = True
        json_data[str_user_id]['group_title'] = message.text
        self.write_json_data(json_data)
        return json_data

    def deactivate_group_description_and_write_itself(self, message: Message) -> dict:
        str_user_id = str(message.from_user.id)
        json_data = self.read_json_file()
        json_data[str_user_id]['set_group_description'] = False
        json_data[str_user_id]['group_description'] = message.text
        self.write_json_data(json_data)
        return json_data

    def deactivate_group_description_and_activate_title(self, user_id: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.read_json_file()
        json_data[str_user_id]['set_group_title'] = True
        json_data[str_user_id]['set_group_description'] = False
        self.write_json_data(json_data)
        return json_data

    def write_last_watering_date(self, user_id: int, last_watering_date: str) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['last_watering_date'] = last_watering_date
        self.write_json_data(json_data)
        return json_data

    def activate_flower_title(self, user_id: int) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['set_flower_title'] = True
        self.write_json_data(json_data)
        return json_data

    def deactivate_flower_title(self, user_id: int) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['set_flower_title'] = False
        self.write_json_data(json_data)
        return json_data

    def activate_flower_description(self, user_id: int) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['set_flower_description'] = True
        self.write_json_data(json_data)
        return json_data

    def activate_flower_description_and_write_title(self, message: Message) -> dict:
        str_user_id = str(message.from_user.id)
        json_data = self.read_json_file()
        json_data[str_user_id]['set_flower_title'] = False
        json_data[str_user_id]['set_flower_description'] = True
        json_data[str_user_id]['flower_title'] = message.text
        self.write_json_data(json_data)
        return json_data

    def deactivate_flower_description_and_write_itself(self, message: Message) -> dict:
        str_user_id = str(message.from_user.id)
        json_data = self.read_json_file()
        json_data[str_user_id]['set_flower_description'] = False
        json_data[str_user_id]['flower_description'] = message.text
        self.write_json_data(json_data)
        return json_data

    def deactivate_flower_description_and_activate_title(self, user_id: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.read_json_file()
        json_data[str_user_id]['set_flower_title'] = True
        json_data[str_user_id]['set_flower_description'] = False
        self.write_json_data(json_data)
        return json_data

    def write_flower_group_title_and_id(self, flower_group: Type[FlowersGroup], user_id: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.read_json_file()
        json_data[str_user_id]['flower_group_id'] = flower_group.id
        json_data[str_user_id]['flower_group_title'] = flower_group.title
        self.write_json_data(json_data)
        return json_data

    def activate_flower_photo(self, user_id: int) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['set_flower_photo'] = True
        self.write_json_data(json_data)
        return json_data

    def deactivate_flower_photo(self, user_id: int) -> tuple[int, dict]:
        str_user_id = str(user_id)
        json_data = self.read_json_file()
        json_data[str_user_id]['set_flower_photo'] = False
        flower_id = json_data[str_user_id].get('flower_id', 0)
        self.write_json_data(json_data)
        return flower_id, json_data

    def activate_refactor_flower_title(self, user_id: int, flower_id: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.write_flower_id(user_id=user_id, flower_id=flower_id)
        json_data[str_user_id]['set_flower_title'] = True
        json_data[str_user_id]['refactor'] = True
        self.write_json_data(json_data)
        return json_data

    def deactivate_refactor_flower_title(self, message: Message) -> tuple[int, str, dict]:
        str_user_id = str(message.from_user.id)
        flower_title = message.text
        json_data = self.read_json_file()
        json_data[str_user_id]['set_flower_title'] = False
        json_data[str_user_id]['refactor'] = False
        json_data[str_user_id]['flower_title'] = flower_title
        flower_id = json_data[str_user_id]['flower_id']
        self.write_json_data(json_data)
        return flower_id, flower_title, json_data

    def activate_refactor_flower_description(self, user_id: int, flower_id: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.write_flower_id(user_id=user_id, flower_id=flower_id)
        json_data[str_user_id]['set_flower_description'] = True
        json_data[str_user_id]['refactor'] = True
        self.write_json_data(json_data)
        return json_data

    def deactivate_refactor_flower_description(self, message: Message) -> tuple[int, str, dict]:
        str_user_id = str(message.from_user.id)
        flower_description = message.text
        json_data = self.read_json_file()
        json_data[str_user_id]['set_flower_description'] = False
        json_data[str_user_id]['refactor'] = False
        json_data[str_user_id]['flower_description'] = flower_description
        flower_id = json_data[str_user_id]['flower_id']
        self.write_json_data(json_data)
        return flower_id, flower_description, json_data

    def activate_refactor_flower_photo(self, user_id: int, flower_id: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.write_flower_id(user_id=user_id, flower_id=flower_id)
        json_data[str_user_id]['set_flower_photo'] = True
        json_data[str_user_id]['refactor'] = True
        self.write_json_data(json_data)
        return json_data

    def deactivate_refactor_flower_photo(self, user_id: int) -> tuple[int, dict]:
        str_user_id = str(user_id)
        json_data = self.read_json_file()
        json_data[str_user_id]['set_flower_photo'] = False
        json_data[str_user_id]['refactor'] = False
        flower_id = json_data[str_user_id]['flower_id']
        self.write_json_data(json_data)
        return flower_id, json_data

    def write_flower_id(self, user_id: int, flower_id: int) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['flower_id'] = flower_id
        self.write_json_data(json_data)
        return json_data

    def activate_refactor_group_title(self, user_id: int, group_id: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.write_group_id(user_id=user_id, group_id=group_id)
        json_data[str_user_id]['set_group_title'] = True
        json_data[str_user_id]['refactor'] = True
        self.write_json_data(json_data)
        return json_data

    def deactivate_refactor_group_title(self, message: Message) -> tuple[int, str, dict]:
        str_user_id = str(message.from_user.id)
        group_title = message.text
        json_data = self.read_json_file()
        json_data[str_user_id]['set_group_title'] = False
        json_data[str_user_id]['refactor'] = False
        json_data[str_user_id]['group_title'] = group_title
        group_id = json_data[str_user_id]['group_id']
        self.write_json_data(json_data)
        return group_id, group_title, json_data

    def activate_refactor_group_description(self, user_id: int, group_id: int) -> dict:
        str_user_id = str(user_id)
        json_data = self.write_group_id(user_id=user_id, group_id=group_id)
        json_data[str_user_id]['set_group_description'] = True
        json_data[str_user_id]['refactor'] = True
        self.write_json_data(json_data)
        return json_data

    def deactivate_refactor_group_description(self, message: Message) -> tuple[int, str, dict]:
        str_user_id = str(message.from_user.id)
        group_description = message.text
        json_data = self.read_json_file()
        json_data[str_user_id]['set_group_description'] = False
        json_data[str_user_id]['refactor'] = False
        json_data[str_user_id]['group_description'] = group_description
        group_id = json_data[str_user_id]['group_id']
        self.write_json_data(json_data)
        return group_id, group_description, json_data

    def write_group_id(self, user_id: int, group_id: int) -> dict:
        json_data = self.read_json_file()
        json_data[str(user_id)]['group_id'] = group_id
        self.write_json_data(json_data)
        return json_data

    def get_json_and_group_id(self, user_id: int) -> tuple[dict, int]:
        json_data = self.read_json_file()
        group_id = json_data[str(user_id)]['group_id']
        return json_data, group_id
