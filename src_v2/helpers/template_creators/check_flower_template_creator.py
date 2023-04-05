from src_v2.helpers.template_creators.base_template_creator import BaseTemplateCreator


class CheckFlowerTemplateCreator(BaseTemplateCreator):

    @staticmethod
    def check_flower_selection(empty_flowers: bool) -> str:
        if empty_flowers:
            return 'Пожалуйста, выберите растения для дальнейших действий:'
        else:
            return 'Вы еще не добавили ни одного растения! Пожалуйста, добавьте растение:'

    @staticmethod
    def check_flower_action(flower_description: str) -> str:
        return f'{flower_description}\n\n Пожалуйста, выберите действие для данного растения:'

    @staticmethod
    def check_flower_confirm_delete(flower_description: str) -> str:
        return f'{flower_description}\n\n Вы действительно хотите удалить данное растение?'

    @staticmethod
    def check_flower_choose_changing_point(flower_description: str) -> str:
        return f'{flower_description}\n\n Пожалуйста, выберите пункт для редактирования данного растения:'

    @staticmethod
    def check_flower_change_title(flower_description: str) -> str:
        return f'{flower_description}\n\n Пожалуйста, отправьте боту сообщение с новым названием для данного растения:'

    @staticmethod
    def check_flower_change_description(flower_description: str) -> str:
        return f'{flower_description}\n\n Пожалуйста, отправьте боту сообщение с новыми заметками для данного растения:'

    @staticmethod
    def check_flower_change_photo(flower_description: str) -> str:
        return f'{flower_description}\n\n Пожалуйста, отправьте боту новую фотографию для данного растения:'

    @staticmethod
    def check_flower_change_group(flower_description: str) -> str:
        return f'{flower_description}\n\n Пожалуйста, выберите сценарий полива для данного растения:'
