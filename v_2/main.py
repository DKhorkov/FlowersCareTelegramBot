import pickle

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
from helpers.photo_processor import PhotoProcessor
from helpers.database_parser import DatabaseParser
from sql_alchemy.adapter import SQLAlchemyAdapter


logger = get_logger('bot_logs')
bot = TeleBot(token=TOKEN)
json_name = 'users_data_json'
calendar = CustomizedCalendar(language=RUSSIAN_LANGUAGE)
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")
sql_alchemy = SQLAlchemyAdapter(logger=logger)
sql_alchemy.create_tables()


"""
    Ниже идет стартовая логика.
"""


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
def add_group_call_query(call):
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
    Ниже идет логика по добавлению цветков.
"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_flower'))
def add_flower_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()
            json[str_user_id]['set_flower_title'] = True
            JsonHandler(json_name).write_json_data(json)

            bot.edit_message_media(
                chat_id=call.from_user.id,
                message_id=json[str_user_id]['message_for_update'],
                reply_markup=MarkupCreator().add_flower_title_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_flower_title(),
                    parse_mode='HTML'
                )
            )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('flower_adding_title'))
def add_flower_title_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                json[str_user_id]['set_flower_title'] = False
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('flower_adding_description'))
def add_flower_description_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                json[str_user_id]['set_flower_title'] = True
                json[str_user_id]['set_flower_description'] = False
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_flower_title_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_flower_title(),
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('flower_adding_group'))
def add_flower_group_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                json[str_user_id]['set_flower_description'] = True
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_flower_description_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_flower_description(
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

            elif "add_group" in call.data:
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

            else:
                flower_group_title = call.data.split(" ")[-2]
                flower_group_id = call.data.split(" ")[-1]
                json[str_user_id]['flower_group_title'] = flower_group_title
                json[str_user_id]['flower_group_id'] = flower_group_id
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_flower_ask_photo_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_flower_ask_photo(
                            json=json,
                            str_user_id=str_user_id
                        ),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('flower_adding_ask_photo'))
def add_flower_photo_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                flowers_groups = sql_alchemy.get_flowers_groups(call.from_user.id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_flower_group_markup(
                        flowers_groups=flowers_groups
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_flower_group(
                            json=json,
                            str_user_id=str_user_id,
                            empty_groups=True if len(flowers_groups) > 0 else False
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

            elif 'yes' in call.data:
                json[str_user_id]['set_flower_photo'] = True
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_flower_photo_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_flower_photo(
                            json=json,
                            str_user_id=str_user_id
                        ),
                        parse_mode='HTML'
                    )
                )

            elif 'no' in call.data:
                with open('static/images/base_flower_photo.jpg', 'rb') as file:
                    photo = file.read()

                sql_alchemy.add_flower(
                    str_user_id=str_user_id,
                    json_data=json,
                    bytes_photo=pickle.dumps(photo)
                )

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().back_to_menu_markup(),
                    media=InputMediaPhoto(
                        media=photo,
                        caption=TemplateCreator().flower_created(
                            json=json,
                            str_user_id=str_user_id
                        ),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('flower_adding_photo'))
def add_flower_photo_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                json[str_user_id]['set_flower_photo'] = False
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_flower_ask_photo_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_flower_ask_photo(
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

    except Exception as e:
        logger.error(e)


"""
    Ниже идет логика по просмотру, редактированию и удалению растений.
"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flowers'))
def check_flowers_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            user_flowers = sql_alchemy.get_user_flowers(call.from_user.id)

            bot.edit_message_media(
                chat_id=call.from_user.id,
                message_id=json[str_user_id]['message_for_update'],
                reply_markup=MarkupCreator().check_flower_selection_markup(
                    user_flowers=user_flowers
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_flower_selection(
                        empty_flowers=True if len(user_flowers) > 0 else False
                    ),
                    parse_mode='HTML'
                )
            )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_selection'))
def check_flower_selection_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
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

            elif 'add_flower' in call.data:
                json[str_user_id]['set_flower_title'] = True
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().add_flower_title_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_flower_title(),
                        parse_mode='HTML'
                    )
                )

            else:
                flower_id = int(call.data.split(' ')[-1])
                flower = sql_alchemy.get_flower(flower_id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_flower_action_markup(
                        flower_id=flower_id
                    ),
                    media=InputMediaPhoto(
                        media=pickle.loads(flower.photo),
                        caption=TemplateCreator().check_flower_action(
                            flower_description=DatabaseParser.parse_flower(
                                sql_alchemy_adapter=sql_alchemy,
                                flower=flower
                            )
                        ),
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

    elif json[str_user_id]['set_flower_title']:
        json[str_user_id]['set_flower_title'] = False
        json[str_user_id]['set_flower_description'] = True
        json[str_user_id]['flower_title'] = message.text
        JsonHandler(json_name).write_json_data(json)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=MarkupCreator().add_flower_description_markup(),
            media=InputMediaPhoto(
                media=open('static/images/media_message_picture.png', 'rb'),
                caption=TemplateCreator().add_flower_description(
                    json=json,
                    str_user_id=str_user_id
                ),
                parse_mode='HTML'
            )
        )

    elif json[str_user_id]['set_flower_description']:
        json[str_user_id]['set_flower_description'] = False
        json[str_user_id]['flower_description'] = message.text
        JsonHandler(json_name).write_json_data(json)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        flowers_groups = sql_alchemy.get_flowers_groups(message.from_user.id)
        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
                reply_markup=MarkupCreator().add_flower_group_markup(
                flowers_groups=flowers_groups
            ),
            media=InputMediaPhoto(
                media=open('static/images/media_message_picture.png', 'rb'),
                caption=TemplateCreator().add_flower_group(
                    json=json,
                    str_user_id=str_user_id,
                    empty_groups=True if len(flowers_groups) > 0 else False
                ),
                parse_mode='HTML'
            )
        )

    else:
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )


@bot.message_handler(content_types= ['photo'])
def photo_messages_handler(message):
    str_user_id = str(message.from_user.id)
    json = JsonHandler(json_name).read_json_file()

    if json.get(str_user_id, None) is None:
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        return

    if json[str_user_id]['set_flower_photo']:
        json[str_user_id]['set_flower_photo'] = False
        JsonHandler(json_name).write_json_data(json)

        photo = bot.get_file(message.photo[-1].file_id)
        bytes_photo = PhotoProcessor.get_photo_from_message(photo)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        sql_alchemy.add_flower(
            str_user_id=str_user_id,
            json_data=json,
            bytes_photo=bytes_photo
        )

        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=MarkupCreator().back_to_menu_markup(),
            media=InputMediaPhoto(
                media=pickle.loads(bytes_photo),
                caption=TemplateCreator().flower_created(
                    json=json,
                    str_user_id=str_user_id
                ),
                parse_mode='HTML'
            )
        )

    else:
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )


@bot.message_handler(content_types= ['document', 'audio', 'video', 'sticker', 'video_note',
                                     'voice', 'location', 'contact'])
def dump_messages_handler(message):
    bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.id
    )


if __name__ == '__main__':
    bot.infinity_polling(timeout=100)
