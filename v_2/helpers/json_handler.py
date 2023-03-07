import json
import os


class JsonHandler:

    def __init__(self, json_name):
        self.json = json_name

    def read_json_file(self):
        if not os.path.exists('JSON_data'):
            os.mkdir('JSON_data')

        if not os.path.exists(f'JSON_data/{self.json}'):
            with open(f'JSON_data/{self.json}', 'w') as file:
                file.write(json.dumps({}))

        with open(f'JSON_data/{self.json}', 'r') as file:
            json_data = json.loads(file.read())

        return json_data

    def write_json_data(self, updated_json):
        if not os.path.exists('JSON_data'):
            os.mkdir('JSON_data')

        with open(f'JSON_data/{self.json}', 'w') as file:
            file.write(json.dumps(updated_json))

    def reset_appropriate_messages(self, str_user_id):
        json_data = self.read_json_file()
        json_data[str_user_id]['set_group_name'] = False
        json_data[str_user_id]['set_group_description'] = False
        json_data[str_user_id]['set_flower_name'] = False
        json_data[str_user_id]['set_flower_description'] = False
        self.write_json_data(json_data)