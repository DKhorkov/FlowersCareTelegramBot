from datetime import datetime


class BaseTemplateCreator:

    @staticmethod
    def base_template() -> str:
        return 'Пожалуйста, выберите действие:'

    @staticmethod
    def _transform_to_russian_date(str_date: str) -> str:
        datetime_date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
        processed_date = datetime.strftime(datetime_date, '%d-%m-%Y')
        return processed_date