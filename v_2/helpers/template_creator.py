from datetime import datetime

class TemplateCreator:

    @staticmethod
    def base_template():
        return 'Пожалуйста, выберите действие:'

    @staticmethod
    def add_group_title():
        return 'Пожалуйста, отправьте боту сообщение с названием сценария полива для ваших цветов:'

    @staticmethod
    def add_group_description(json, str_user_id):
        template = f"<b>Название сценария полива:</b> {json[str_user_id]['group_title']}\n\n" \
                   f"Пожалуйста, отправьте боту сообщение с описанием сценария полива для ваших цветов:"
        return template

    @staticmethod
    def add_group_watering_last_time(json, str_user_id):
        template = f"<b>Название сценария полива:</b> {json[str_user_id]['group_title']}\n" \
                   f"<b>Описание сценария полива:</b> {json[str_user_id]['group_description']}\n\n" \
                   f"Пожалуйста, выберите дату последнего полива для создаваемого сценария:"
        return template

    @staticmethod
    def add_group_watering_interval(json, str_user_id):
        template = f"<b>Название сценария полива:</b> {json[str_user_id]['group_title']}\n" \
                   f"<b>Описание сценария полива:</b> {json[str_user_id]['group_description']}\n" \
                   f"<b>Дата последнего полива:</b> {json[str_user_id]['last_time_watering_date'].split(' ')[0]}\n\n" \
                   f"Пожалуйста, выберите интервал полива для создаваемого сценария:"
        return template

    def group_created(self, json, str_user_id):
        template = f"✅ <b>Сценарий полива успешно создан:</b> ✅\n\n" \
                   f"<b>Название сценария полива:</b> {json[str_user_id]['group_title']}\n" \
                   f"<b>Описание сценария полива:</b> {json[str_user_id]['group_description']}\n" \
                   f"<b>Дата последнего полива:</b> " \
                   f"{self.__transform_to_russian_date(json[str_user_id]['last_time_watering_date'])}\n" \
                   f"<b>Интервал полива:</b> {json[str_user_id]['watering_interval']}\n" \
                   f"<b>Дата следующего полива:</b> " \
                   f"{self.__transform_to_russian_date(json[str_user_id]['next_watering_date'])}\n\n"
        return template

    @staticmethod
    def __transform_to_russian_date(str_date):
        datetime_date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
        processed_date = datetime.strftime(datetime_date, '%d-%m-%Y')
        return processed_date
