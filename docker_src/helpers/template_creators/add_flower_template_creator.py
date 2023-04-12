from .base_template_creator import BaseTemplateCreator


class AddFlowerTemplateCreator(BaseTemplateCreator):

    @staticmethod
    def add_flower_title() -> str:
        return "Пришло время добавить растение🌱\n" \
               "Давай дадим ему имя.\n\n" \
               "Отправь мне сообщение с текстом, и я запомню его как название растения.\n\n"

    def add_flower_description(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_flower_title_text(json=json, str_user_id=str_user_id) +  f'\n'+ \
                   f'Круто, теперь я знаю на одно растение больше😍\n' \
                   f'Добавишь его описание? Чтобы знать наверняка, о каком зеленом речь.\n\n' \
                   f'Отправь мне сообщение с текстом, и я запомню его как описание растения ' \
                   f'<b>{json[str_user_id]["flower_title"]}</b>.\n\n' \
                   f'Если не хочешь добавлять описание, отправь "➖".\n\n'
        return template

    def add_flower_group(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_flower_title_text(json=json, str_user_id=str_user_id) + \
                   self.__generate_flower_description_text(json=json, str_user_id=str_user_id) + \
                   f'Сохранил описание📝\n' \
                   f'Давай закрепим растение за одним из твоих сценариев.\n\n' \
                   f'Выбери ниже название сценария, чтобы закрепить за ним растение ' \
                   f'<b>{json[str_user_id]["flower_title"]}</b>:\n\n'
        return template

    def add_flower_ask_photo(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_all_flower_data_text(json=json, str_user_id=str_user_id) + \
                   f'Замечательно! Теперь я знаю, что твое растение нужно поливать по сценарию ' \
                   f'<b>{json[str_user_id]["flower_group_title"]}</b> 😉\n\n' \
                   f'Хочешь добавить фотографию растения <b>{json[str_user_id]["flower_title"]}</b>?\n\n'
        return template

    def add_flower_photo(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_all_flower_data_text(json=json, str_user_id=str_user_id) + \
                   f'Как классно, что я смогу увидеть твое растение☺️\n\n' \
                   f'Отправь мне фотографию, и я сохраню его как изображение растения ' \
                   f'<b>{json[str_user_id]["flower_title"]}</b>.\n' \
                   f'Если не получилось, проверь, не отправляешь ли фотографию как файл - ' \
                   f'я распознаю только изображения.\n\n'
        return template

    def add_flower_confirm_data(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_all_flower_data_text(json=json, str_user_id=str_user_id) + \
                   f'Запомнил!\n' \
                   f'Подтверди, все ли верно?\n\n'
        return template

    def flower_created(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_all_flower_data_text(json=json, str_user_id=str_user_id) + \
                   f'Поздравляю!\n' \
                   f'Твое растение успешно добавлено ✅\n\n'
        return template

    @staticmethod
    def __generate_flower_title_text(json: dict, str_user_id: str) -> str:
        flower_title_text = f'<b>Растение:</b> {json[str_user_id]["flower_title"]}\n'
        return flower_title_text

    @staticmethod
    def __generate_flower_description_text(json: dict, str_user_id: str) -> str:
        flower_description_text = f'<b>Описание растения:</b> {json[str_user_id]["flower_description"]}\n\n'
        return flower_description_text

    @staticmethod
    def __generate_flower_group_title_text(json: dict, str_user_id: str) -> str:
        flower_group_title_text = f'<b>Сценарий полива:</b> {json[str_user_id]["flower_group_title"]}\n\n'
        return flower_group_title_text

    def __generate_all_flower_data_text(self, json: dict, str_user_id: str) -> str:
        all_flower_data_text = self.__generate_flower_title_text(json=json, str_user_id=str_user_id) + \
                               self.__generate_flower_description_text(json=json, str_user_id=str_user_id) + \
                               self.__generate_flower_group_title_text(json=json, str_user_id=str_user_id)
        return all_flower_data_text
