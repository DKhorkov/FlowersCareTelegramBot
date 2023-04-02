from datetime import datetime


class BaseTemplateCreator:

    @staticmethod
    def base_template() -> str:
        return f'Привет!\n' \
               f'Кажется, ты хочешь отрегулировать полив растений😃\n' \
               f'Я тебе помогу.\n\n' \
               f'Выбери действие ниже, чтобы мы могли продолжить:\n\n'

    @staticmethod
    def _transform_to_russian_date(str_date: str) -> str:
        datetime_date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
        processed_date = datetime.strftime(datetime_date, '%d-%m-%Y')
        return processed_date