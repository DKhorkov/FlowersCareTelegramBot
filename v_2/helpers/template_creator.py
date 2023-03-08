from datetime import datetime

class TemplateCreator:

    @staticmethod
    def base_template():
        return 'Пожалуйста, выберите действие:'

    @staticmethod
    def add_group_name():
        return 'Пожалуйста, отправьте боту сообщение с названием группы для ваших цветов:'

    @staticmethod
    def add_group_description(json, str_user_id):
        template = f"Название группы: {json[str_user_id]['group_name']}\n\n" \
                   f"Пожалуйста, отправьте боту сообщение с описанием группы для ваших цветов:"
        return template

    @staticmethod
    def add_group_watering_last_time(json, str_user_id):
        template = f"Название группы: {json[str_user_id]['group_name']}\n" \
                   f"Описание группы: {json[str_user_id]['group_description']}\n\n" \
                   f"Пожалуйста, выберите последнюю дату полива для создаваемой группы:"
        return template

    @staticmethod
    def add_group_watering_interval(json, str_user_id):
        template = f"Название группы: {json[str_user_id]['group_name']}\n" \
                   f"Описание группы: {json[str_user_id]['group_description']}\n" \
                   f"Последняя дата полива группы: {json[str_user_id]['last_time_watering_date'].split(' ')[0]}\n\n" \
                   f"Пожалуйста, выберите интервал полива для создаваемой группы:"
        return template

    def group_created(self, json, str_user_id):
        template = f"✅ <b>Группа успешно создана:</b> ✅\n\n" \
                   f"Название группы: {json[str_user_id]['group_name']}\n" \
                   f"Описание группы: {json[str_user_id]['group_description']}\n" \
                   f"Последняя дата полива группы: " \
                   f"{self.__transform_to_russian_date(json[str_user_id]['last_time_watering_date'])}\n" \
                   f"Интервал полива: {json[str_user_id]['watering_interval']}\n" \
                   f"Дата следующего полива: " \
                   f"{self.__transform_to_russian_date(json[str_user_id]['next_watering_date'])}\n\n"
        return template

    @staticmethod
    def __transform_to_russian_date(str_date):
        datetime_date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
        processed_date = datetime.strftime(datetime_date, '%d-%m-%Y')
        return processed_date
