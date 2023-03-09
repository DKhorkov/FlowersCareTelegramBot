from datetime import datetime

class BaseTemplateCreator:

    @staticmethod
    def base_template() -> str:
        return 'Пожалуйста, выберите действие:'


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
                   f"<b>Дата последнего полива:</b> {json[str_user_id]['last_time_watering_date'].split(' ')[0]}\n\n" \
                   f"Пожалуйста, выберите интервал полива для создаваемого сценария:"
        return template

    def group_created(self, json: dict, str_user_id: str) -> str:
        template = f"✅ <b>Сценарий полива успешно добавлен:</b> ✅\n\n" \
                   f"<b>Название сценария полива:</b> {json[str_user_id]['group_title']}\n" \
                   f"<b>Описание сценария полива:</b> {json[str_user_id]['group_description']}\n" \
                   f"<b>Дата последнего полива:</b> " \
                   f"{self.__transform_to_russian_date(json[str_user_id]['last_time_watering_date'])}\n" \
                   f"<b>Интервал полива:</b> {json[str_user_id]['watering_interval']}\n" \
                   f"<b>Дата следующего полива:</b> " \
                   f"{self.__transform_to_russian_date(json[str_user_id]['next_watering_date'])}\n\n"
        return template

    @staticmethod
    def __transform_to_russian_date(str_date: str) -> str:
        datetime_date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
        processed_date = datetime.strftime(datetime_date, '%d-%m-%Y')
        return processed_date


class AddFlowerTemplateCreator(BaseTemplateCreator):

    @staticmethod
    def add_flower_title() -> str:
        return 'Пожалуйста, отправьте боту сообщение с названием растения:'

    @staticmethod
    def add_flower_description(json: dict, str_user_id: str) -> str:
        template = f"<b>Название растения:</b> {json[str_user_id]['flower_title']}\n\n" \
                   f"Пожалуйста, отправьте боту сообщение с заметками по растению:"
        return template

    @staticmethod
    def add_flower_group(json: dict, str_user_id: str, empty_groups: bool) -> str:
        template = f"<b>Название растения:</b> {json[str_user_id]['flower_title']}\n" \
                   f"<b>Заметки по растению:</b> {json[str_user_id]['flower_description']}\n\n"

        if not empty_groups:
            template += "Пожалуйста, выберите сценарий полива, к которому необходимо отнести данное растение:"
        else:
            template += "Вы пока не создали ни одного сценария полива. Пожалуйста, создайте сценарий полива!"

        return template

    @staticmethod
    def add_flower_ask_photo(json: dict, str_user_id: str) -> str:
        template = f"<b>Название растения:</b> {json[str_user_id]['flower_title']}\n" \
                   f"<b>Заметки по растению:</b> {json[str_user_id]['flower_description']}\n" \
                   f"<b>Сценарий полива:</b> {json[str_user_id]['flower_group_title']}\n\n" \
                   f"Вы хотите добавить фотографию растения?"
        return template

    @staticmethod
    def add_flower_photo(json: dict, str_user_id: str) -> str:
        template = f"<b>Название растения:</b> {json[str_user_id]['flower_title']}\n" \
                   f"<b>Заметки по растению:</b> {json[str_user_id]['flower_description']}\n" \
                   f"<b>Сценарий полива:</b> {json[str_user_id]['flower_group_title']}\n\n" \
                   f"Пожалуйста, отправьте боту фотографию данного растения:"
        return template

    @staticmethod
    def flower_created(json: dict, str_user_id: str) -> str:
        template = f"✅ <b>Растение успешно добавлено:</b> ✅\n\n" \
                   f"<b>Название растения:</b> {json[str_user_id]['flower_title']}\n" \
                   f"<b>Заметки по растению:</b> {json[str_user_id]['flower_description']}\n" \
                   f"<b>Сценарий полива:</b> {json[str_user_id]['flower_group_title']}\n\n"
        return template


class CheckFlowerTemplateCreator(BaseTemplateCreator):

    @staticmethod
    def check_flower_selection(empty_flowers: bool) -> str:
        if empty_flowers:
            return 'Пожалуйста, выберите растения для дальнейших действий:'
        else:
            return 'Вы еще не добавили ни одного растения! Пожалуйста, добавьте растение:'

    @staticmethod
    def check_flower_action(flower_description: str) -> str:
        return f'{flower_description}\n\n Пожалуйста, выберите действие:'


class TemplateCreator(AddGroupTemplateCreator, AddFlowerTemplateCreator, CheckFlowerTemplateCreator):
    pass
