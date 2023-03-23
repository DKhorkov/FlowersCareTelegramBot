from v_2.helpers.template_creators.base_template_creator import BaseTemplateCreator


class AddFlowerTemplateCreator(BaseTemplateCreator):

    @staticmethod
    def add_flower_no_groups() -> str:
        return "Вы пока не создали ни одного сценария полива. Пожалуйста, создайте сценарий полива!"

    @staticmethod
    def add_flower_title() -> str:
        return "Пожалуйста, отправьте боту сообщение с названием растения:"

    @staticmethod
    def add_flower_description(json: dict, str_user_id: str) -> str:
        template = f"<b>Название растения:</b> {json[str_user_id]['flower_title']}\n\n" \
                   f"Пожалуйста, отправьте боту сообщение с заметками по растению:"
        return template

    @staticmethod
    def add_flower_group(json: dict, str_user_id: str) -> str:
        template = f"<b>Название растения:</b> {json[str_user_id]['flower_title']}\n" \
                   f"<b>Заметки по растению:</b> {json[str_user_id]['flower_description']}\n\n" \
                   f"Пожалуйста, выберите сценарий полива, к которому необходимо отнести данное растение:"
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
        template = f"✅ <b>Растение успешно добавлено:</b>\n\n" \
                   f"<b>Название растения:</b> {json[str_user_id]['flower_title']}\n" \
                   f"<b>Заметки по растению:</b> {json[str_user_id]['flower_description']}\n" \
                   f"<b>Сценарий полива:</b> {json[str_user_id]['flower_group_title']}\n\n"
        return template
