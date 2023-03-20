from v_2.helpers.json_handler import JsonHandler
from v_2.configs import json_name


class JsonApi:

    def __init__(self, user_id: int) -> None:
        self.__user_id = user_id
        self.__str_user_id = str(self.__user_id)
        self.__json_data = JsonHandler(json_name).read_json_file()
        self.__user_json_data = self.__json_data.get(self.__str_user_id, dict())
        self.refactor = self.__user_json_data.get('refactor', False)
        self.set_flower_title = self.__user_json_data.get('set_flower_title', False)
        self.set_flower_description = self.__user_json_data.get('set_flower_description', False)
        self.set_flower_photo = self.__user_json_data.get('set_flower_photo', False)
        self.set_group_title = self.__user_json_data.get('set_group_title', False)
        self.set_group_description = self.__user_json_data.get('set_group_description', False)
        self.flower_id = self.__user_json_data.get('flower_id', 0)
