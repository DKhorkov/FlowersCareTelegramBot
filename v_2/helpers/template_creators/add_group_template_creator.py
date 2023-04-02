from v_2.helpers.template_creators.base_template_creator import BaseTemplateCreator


class AddGroupTemplateCreator(BaseTemplateCreator):

    @staticmethod
    def add_group_title() -> str:
        return 'Ура, ты добавляешь сценарий полива🚿\n' \
               'Давай придумаем ему название.\n\n' \
               'Отправь мне сообщение с текстом, и я запомню его как название сценария.\n\n'

    def add_group_description(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_group_title_text(json=json, str_user_id=str_user_id) +  f'\n'+ \
                   f'Есть, название запомнил🤓\n' \
                   f'Давай добавим описание сценария, чтобы потом не запутаться.\n\n' \
                   f'Отправь мне сообщение с текстом, и я запомню его как описание сценария ' \
                   f'<b>{json[str_user_id]["group_title"]}</b>.\n\n' \
                   f'Если не хочешь добавлять описание, отправь "➖".\n\n'
        return template

    def add_group_watering_last_time(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_group_title_text(json=json, str_user_id=str_user_id) + \
                   self.__generate_group_description_text(json=json, str_user_id=str_user_id) + \
                   f'Отлично, я записал твои заметки о сценарии📝\n' \
                   f'Теперь давай занесем данные о поливе.\n\n' \
                   f'Отметь в календаре день последнего полива растений, которые в дальнейшем закрепишь за сценарием ' \
                   f'<b>{json[str_user_id]["group_title"]}</b>.\n\n'
        return template

    def add_group_watering_interval(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_group_title_text(json=json, str_user_id=str_user_id) + \
                   self.__generate_group_description_text(json=json, str_user_id=str_user_id) + \
                   self.__generate_group_last_watering_date_text(json=json, str_user_id=str_user_id) + f'\n' \
                   f'Хорошо, теперь мне известен день последнего полива📅\n' \
                   f'Но как часто нужно поливать растения из этого сценария?\n\n' \
                   f'Выбери ниже длительность интервала между поливами для сценария ' \
                   f'<b>{json[str_user_id]["group_title"]}</b>.\n\n'
        return template

    def add_group_confirm_data(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_all_group_data_text(json=json, str_user_id=str_user_id) + \
                   f'Запомнил!\n' \
                   f'Подтверди, все ли верно?\n\n'
        return template

    def group_created(self, json: dict, str_user_id: str) -> str:
        template = self.__generate_all_group_data_text(json=json, str_user_id=str_user_id) + \
                   f'Поздравляю!\n' \
                   f'Твой сценарий полива успешно добавлен ✅\n\n'
        return template

    @staticmethod
    def __generate_group_title_text(json: dict, str_user_id: str) -> str:
        group_title_text = f'<b>Cценарий полива:</b> {json[str_user_id]["group_title"]}\n'
        return group_title_text

    @staticmethod
    def __generate_group_description_text(json: dict, str_user_id: str) -> str:
        group_description_text = f'<b>Описание сценария полива:</b> {json[str_user_id]["group_description"]}\n\n'
        return group_description_text

    def __generate_group_last_watering_date_text(self, json: dict, str_user_id: str) -> str:
        group_last_watering_date_text = f'<b>Дата последнего полива:</b> ' \
                                        f'{self._transform_to_russian_date(json[str_user_id]["last_watering_date"])}\n'
        return group_last_watering_date_text

    def __generate_all_group_data_text(self, json: dict, str_user_id: str) -> str:
        all_group_data_text = self.__generate_group_title_text(json=json, str_user_id=str_user_id) + \
                              self.__generate_group_description_text(json=json, str_user_id=str_user_id) + \
                              self.__generate_group_last_watering_date_text(json=json, str_user_id=str_user_id) + \
                              f'<b>Интервал между поливами:</b> {json[str_user_id]["watering_interval"]}\n\n' \
                              f'<b>Дата следующего полива:</b> ' \
                              f'{self._transform_to_russian_date(json[str_user_id]["next_watering_date"])}\n\n'
        return all_group_data_text
