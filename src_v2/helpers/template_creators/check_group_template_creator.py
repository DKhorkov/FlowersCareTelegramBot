from src_v2.helpers.template_creators.base_template_creator import BaseTemplateCreator


class CheckGroupTemplateCreator(BaseTemplateCreator):

    @staticmethod
    def check_group_selection(empty_groups: bool) -> str:
        if empty_groups:
            return 'Пожалуйста, выберите сценарий полива растений для дальнейших действий:'
        else:
            return 'Вы еще не добавили ни одного сценария полива растений! Пожалуйста, добавьте сценарий полива:'

    @staticmethod
    def check_group_action(group_description: str) -> str:
        return f'{group_description}\n\n Пожалуйста, выберите действие для данного сценария полива:'

    @staticmethod
    def check_group_confirm_delete(group_description: str) -> str:
        return f'{group_description}\n\n Вы действительно хотите удалить данный сценарий полива?'

    @staticmethod
    def check_group_choose_changing_point(group_description: str) -> str:
        return f'{group_description}\n\n Пожалуйста, выберите пункт для редактирования данного сценария полива:'

    @staticmethod
    def check_group_change_title(group_description: str) -> str:
        return f'{group_description}\n\n Пожалуйста, отправьте боту сообщение с новым названием для данного сценария ' \
               f'полива:'

    @staticmethod
    def check_group_change_description(group_description: str) -> str:
        return f'{group_description}\n\n Пожалуйста, отправьте боту сообщение с новым описанием для данного сценария ' \
               f'полива:'

    @staticmethod
    def check_group_change_watering_interval(group_description: str) -> str:
        return f'{group_description}\n\n Пожалуйста, выберите новый интервал полива для данного сценария:'

    @staticmethod
    def check_group_change_last_watering_date(group_description: str) -> str:
        return f'{group_description}\n\n Пожалуйста, выберите обновленную дату последнего полива для данного сценария:'

    @staticmethod
    def check_group_see_flowers(group_description: str, group_flowers_length: int) -> str:
        if group_flowers_length != 0:
            return f'{group_description}\n\n Пожалуйста, выберите растение данного сценария полива для просмотра:'
        else:
            return f'{group_description}\n\n Вы еще не добавили ни одного растения в данный сценарий полива!'
