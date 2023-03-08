from telebot import TeleBot
from telebot.types import InputMediaPhoto
from datetime import datetime, timedelta

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
from sql_alchemy.adapter import SQLAlchemyAdapter


logger = get_logger('bot_logs')
bot = TeleBot(token=TOKEN)
json_name = 'users_data_json'
calendar = CustomizedCalendar(language=RUSSIAN_LANGUAGE)
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")
sql_alchemy = SQLAlchemyAdapter(logger=logger)
sql_alchemy.create_tables()


@bot.message_handler(commands=["start"])
def start(message):

    if sql_alchemy.check_if_user_already_registered(message.from_user.id):
        sql_alchemy.add_user(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            is_bot=message.from_user.is_bot
        )
        #TODO Добавить приветственное сообщение с отправкой инфы по боту и его командам. Создать команду --help

    str_user_id = str(message.from_user.id)
    json_data = JsonHandler(json_name).read_json_file()

    message_to_update = bot.send_media_group(
        chat_id=message.from_user.id,
        media=[
            InputMediaPhoto(
            media=open('static/images/media_message_picture.png', 'rb'),
            caption=TemplateCreator().base_template(),
            parse_mode='HTML'
        )
        ]
    )[0].id

    bot.edit_message_reply_markup(
        chat_id=message.from_user.id,
        message_id=message_to_update,
        reply_markup=MarkupCreator().base_markup()
    )

    json_data[str_user_id] = {}
    json_data[str_user_id]['message_for_update'] = message_to_update
    JsonHandler(json_name).write_json_data(json_data)
    JsonHandler(json_name).reset_appropriate_messages(str_user_id)


"""
    Ниже идет логика по созданию сценария (группы) полива цветов.
"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_group'))
def creating_group_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()
            json[str_user_id]['set_group_title'] = True
            JsonHandler(json_name).write_json_data(json)

            bot.edit_message_media(
                chat_id=call.from_user.id,
                message_id=json[str_user_id]['message_for_update'],
                reply_markup=MarkupCreator().add_group_title_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_group_title(),
                    parse_mode='HTML'
                )
            )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_title'))
def add_group_title_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                json[str_user_id]['set_group_title'] = False
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().base_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().base_template(),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_description'))
def add_group_description_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                json[str_user_id]['set_group_title'] = True
                json[str_user_id]['set_group_description'] = False
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_group_title_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_group_title(),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().base_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().base_template(),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def add_last_time_watering_call_query(call: CallbackQuery):
    try:
        if call.message:
            json = JsonHandler(json_name).read_json_file()
            str_user_id = str(call.from_user.id)

            name, action, year, month, day = call.data.split(calendar_callback.sep)
            last_time_watering_date = calendar.calendar_query_handler(
                bot=bot,
                call=call,
                name=name,
                action=action,
                year=year,
                month=month,
                day=day
            )

            if action == "DAY":
                json[str_user_id]['last_time_watering_date'] = str(last_time_watering_date)
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_group_watering_interval_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_group_watering_interval(
                            json=json,
                            str_user_id=str_user_id
                        ),
                        parse_mode='HTML'
                    )
                )

            elif action == "MENU":
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().base_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().base_template(),
                        parse_mode='HTML'
                    )
                )

            elif action == "BACK":
                json[str_user_id]['set_group_description'] = True
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_group_description_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_group_description(
                            json=json,
                            str_user_id=str_user_id
                        ),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_interval'))
def add_watering_interval_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                now = datetime.now()

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=calendar.create_calendar(
                        name=calendar_callback.prefix,
                        year=now.year,
                        month=now.month
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_group_watering_last_time(
                            json=json,
                            str_user_id=str_user_id
                        ),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().base_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().base_template(),
                        parse_mode='HTML'
                    )
                )

            else:
                watering_interval = int(call.data.split(' ')[-1])
                JsonHandler(json_name).process_watering_interval(
                    json_data=json,
                    str_user_id=str_user_id,
                    watering_interval=watering_interval
                )

                sql_alchemy.add_flower_group(
                    str_user_id=str_user_id,
                    json_data=JsonHandler(json_name).read_json_file()
                )

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().back_to_menu_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().group_created(
                            json=json,
                            str_user_id=str_user_id
                        ),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('MENU'))
def created_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            bot.edit_message_media(
                chat_id=call.from_user.id,
                message_id=json[str_user_id]['message_for_update'],
                reply_markup=MarkupCreator().base_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().base_template(),
                    parse_mode='HTML'
                )
            )

    except Exception as e:
        logger.error(e)


"""
    Ниже идет логика по просмотру, редактированию и удалению сценариев (групп) полива.
"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_groups'))
def check_groups_call_query(call):
    pass


"""
    Ниже идет логика по обработке сообщений от пользователей.
"""


@bot.message_handler(content_types= ['text'])
def text_messages_handler(message):
    str_user_id = str(message.from_user.id)
    json = JsonHandler(json_name).read_json_file()

    if json.get(str_user_id, None) is None:
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        return

    if json[str_user_id]['set_group_title']:
        json[str_user_id]['set_group_title'] = False
        json[str_user_id]['set_group_description'] = True
        json[str_user_id]['group_title'] = message.text
        JsonHandler(json_name).write_json_data(json)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=MarkupCreator().add_group_description_markup(),
            media=InputMediaPhoto(
                media=open('static/images/media_message_picture.png', 'rb'),
                caption=TemplateCreator().add_group_description(
                    json=json,
                    str_user_id=str_user_id
                ),
                parse_mode='HTML'
            )
        )

    elif json[str_user_id]['set_group_description']:
        json[str_user_id]['set_group_description'] = False
        json[str_user_id]['group_description'] = message.text
        JsonHandler(json_name).write_json_data(json)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        now = datetime.now()
        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=calendar.create_calendar(
                name=calendar_callback.prefix,
                year=now.year,
                month=now.month
            ),
            media=InputMediaPhoto(
                media=open('static/images/media_message_picture.png', 'rb'),
                caption=TemplateCreator().add_group_watering_last_time(
                    json=json,
                    str_user_id=str_user_id
                ),
                parse_mode='HTML'
            )
        )

    else:
        bot.delete_message(message.chat.id, message.message_id)


# TODO убрать отсюда тип-фото сделать для него отдельный обработчик, ибо будем принимать фотку цветов
@bot.message_handler(content_types= ['photo', 'document', 'audio', 'video', 'sticker', 'video_note',
                                     'voice', 'location', 'contact'])
def dump_messages_handler(message):
    bot.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
    bot.infinity_polling(timeout=100)
