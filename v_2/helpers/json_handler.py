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

    def clear_iterables(self, user_id):
        json_data = self.read_json_file()
        json_data[str(user_id)]['platforms'] = []
        json_data[str(user_id)]['metrics'] = []
        if self.json == 'compare_subscribes.json':
            json_data[str(user_id)]['streams_to_check'] = []
            json_data[str(user_id)]['thresholds'] = {}

        self.write_json_data(json)