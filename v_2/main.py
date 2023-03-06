from telebot import TeleBot

from telebot_calendar import CallbackData, RUSSIAN_LANGUAGE
from telebot.types import CallbackQuery
from ast import literal_eval
from threading import Thread

from configs import TOKEN
from helpers.logging_system import get_logger
from helpers.customized_calendar import CustomizedCalendar
from helpers.json_handler import JsonHandler
from helpers.template_creator import TemplateCreator
from helpers.markup_creator import MarkupCreator
from helpers.message_editor import BotMessagesEditor


logger = get_logger('bot_logs')
bot = TeleBot(token=TOKEN)
json_name = 'users_data_json'
mgs_editor = BotMessagesEditor(bot=bot)


@bot.message_handler(commands=["start"])
def start(message):

    # TODO Добавить сохранения данных пользователя в таблицу БД, если юзер еще не подписан

    sticker = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    str_user_id = str(message.from_user.id)
    json_data = JsonHandler(json_name).read_json_file()

    message_to_update = bot.send_message(
        chat_id=message.from_user.id,
        text=TemplateCreator().base_template(),
        reply_markup=MarkupCreator().create_base_markup(),
    ).id

    json_data[str_user_id] = {}
    json_data[str_user_id]['message_for_update'] = message_to_update
    JsonHandler(json_name).write_json_data(json_data)

    logger.info(f'User {message.from_user.id} have been already subscribed!')


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_group'))
def creating_group_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()
            mgs_editor.edit_message(
                user_id=call.from_user.id,
                template_method=TemplateCreator().add_group_name,
                markup_method=MarkupCreator().create_group_adding_markup,
                json=json,
                str_user_id=str_user_id
            )

    except Exception as e:
        logger.info(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_name'))
def creating_group_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                mgs_editor.edit_message(
                    user_id=call.from_user.id,
                    template_method=TemplateCreator().base_template,
                    markup_method=MarkupCreator().create_base_markup,
                    json=json,
                    str_user_id=str_user_id
                )

    except Exception as e:
        logger.info(e)


if __name__ == '__main__':
    bot.infinity_polling(timeout=100)
