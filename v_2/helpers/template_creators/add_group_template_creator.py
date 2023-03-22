from v_2.helpers.template_creators.base_template_creator import BaseTemplateCreator


class AddGroupTemplateCreator(BaseTemplateCreator):

    @staticmethod
    def add_group_title() -> str:
        return 'Пожалуйста, отправьте боту сообщение с названием сценария полива для ваших растений:'

    @staticmethod
    def add_group_description(json: dict, str_user_id: str) -> str:
        template = f"<b>Название сценария полива:</b> {json[str_user_id]['group_title']}\n\n" \
                   f"Пожалуйста, отправьте боту сообщение с описанием сценария полива для ваших растений:"
        return template

    @staticmethod
    def add_group_watering_last_time(json: dict, str_user_id: str) -> str:
        template = f"<b>Название сценария полива:</b> {json[str_user_id]['group_title']}\n" \
                   f"<b>Описание сценария полива:</b> {json[str_user_id]['group_description']}\n\n" \
                   f"Пожалуйста, выберите дату последнего полива для создаваемого сценария:"
        return template

    @staticmethod
    def add_group_watering_interval(json: dict, str_user_id: str) -> str:
        template = f"<b>Название сценария полива:</b> {json[str_user_id]['group_title']}\n" \
                   f"<b>Описание сценария полива:</b> {json[str_user_id]['group_description']}\n" \
                   f"<b>Дата последнего полива:</b> {json[str_user_id]['last_watering_date'].split(' ')[0]}\n\n" \
                   f"Пожалуйста, выберите интервал полива для создаваемого сценария:"
        return template

    def group_created(self, json: dict, str_user_id: str) -> str:
        template = f"✅ <b>Сценарий полива успешно добавлен:</b> ✅\n\n" \
                   f"<b>Название сценария полива:</b> {json[str_user_id]['group_title']}\n" \
                   f"<b>Описание сценария полива:</b> {json[str_user_id]['group_description']}\n" \
                   f"<b>Дата последнего полива:</b> " \
                   f"{self._transform_to_russian_date(json[str_user_id]['last_watering_date'])}\n" \
                   f"<b>Интервал полива:</b> {json[str_user_id]['watering_interval']}\n" \
                   f"<b>Дата следующего полива:</b> " \
                   f"{self._transform_to_russian_date(json[str_user_id]['next_watering_date'])}\n\n"
        return template
