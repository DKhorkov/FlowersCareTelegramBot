import pickle

from telebot import TeleBot
from telebot.types import InputMediaPhoto
from datetime import datetime

from telebot_calendar import CallbackData, RUSSIAN_LANGUAGE
from telebot.types import CallbackQuery
from threading import Thread

from configs import TOKEN, json_name
from helpers.logging_system import get_logger
from helpers.customized_calendar import CustomizedCalendar
from helpers.json_handler import JsonHandler
from helpers.template_creator import TemplateCreator
from helpers.markup_creator import MarkupCreator
from helpers.photo_processor import PhotoProcessor
from helpers.database_parser import DatabaseParser
from helpers.message_handler import MessageHandler
from sql_alchemy.adapter import SQLAlchemyAdapter


bot = TeleBot(token=TOKEN)
logger = get_logger('bot_logs')
sql_alchemy = SQLAlchemyAdapter(logger=logger)
sql_alchemy.create_tables()


calendar = CustomizedCalendar(language=RUSSIAN_LANGUAGE)
create_group_calendar_callback = CallbackData("create_group_calendar", "action", "year", "month", "day")
change_group_calendar_callback = CallbackData("change_group_calendar", "action", "year", "month", "day")



"""
    Ниже идет стартовая логика.
"""


@bot.message_handler(commands=["start"])
def start(message):

    if sql_alchemy.check_if_user_already_registered(message.from_user.id):
        sql_alchemy.add_user(message)
        #TODO Добавить приветственное сообщение с отправкой инфы по боту и его командам. Создать команду --help

    message_for_update = MessageHandler.send_start_message(bot=bot, message=message)
    JsonHandler(json_name).prepare_json(str_user_id=str(message.from_user.id), message_for_update=message_for_update)



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

            MessageHandler.send_add_group_title_message(bot=bot, user_id=call.from_user.id, json=json)

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

                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

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

                MessageHandler.send_add_group_title_message(bot=bot, user_id=call.from_user.id, json=json)

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(create_group_calendar_callback.prefix))
def add_group_last_watering_date_call_query(call: CallbackQuery):
    try:
        if call.message:
            json = JsonHandler(json_name).read_json_file()
            str_user_id = str(call.from_user.id)

            name, action, year, month, day = call.data.split(create_group_calendar_callback.sep)
            last_watering_date = calendar.calendar_query_handler(
                bot=bot,
                call=call,
                name=name,
                action=action,
                year=year,
                month=month,
                day=day
            )

            if action == "DAY":
                json[str_user_id]['last_watering_date'] = str(last_watering_date)
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_add_group_watering_interval_message(bot=bot, user_id=call.from_user.id, json=json)

            elif action == "MENU":
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif action == "BACK":
                json[str_user_id]['set_group_description'] = True
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_add_group_description_message(bot=bot, user_id=call.from_user.id, json=json)

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_interval'))
def add_group_watering_interval_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                MessageHandler.send_add_group_last_watering_date_message(bot=bot, user_id=call.from_user.id, json=json)

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            else:
                watering_interval = int(call.data.split(' ')[-1])
                JsonHandler(json_name).process_watering_interval(
                    json_data=json,
                    str_user_id=str_user_id,
                    watering_interval=watering_interval
                )

                sql_alchemy.add_group(
                    str_user_id=str_user_id,
                    json_data=JsonHandler(json_name).read_json_file()
                )

                MessageHandler.send_add_group_created_message(bot=bot, user_id=call.from_user.id, json=json)

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_created'))
def add_group_created_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'add_flower' in call.data:
                json[str_user_id]['set_flower_title'] = True
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_add_flower_title_message(bot=bot, user_id=call.from_user.id, json=json)

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('MENU'))
def back_to_menu_call_query(call):
    try:
        if call.message:
            json = JsonHandler(json_name).read_json_file()
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

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

            MessageHandler.send_add_flower_title_message(bot=bot, user_id=call.from_user.id, json=json)

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

                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

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

                MessageHandler.send_add_flower_title_message(bot=bot, user_id=call.from_user.id, json=json)

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

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

                MessageHandler.send_add_flower_description_message(bot=bot, user_id=call.from_user.id, json=json)

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif "add_group" in call.data:
                json[str_user_id]['set_group_title'] = True
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_add_group_title_message(bot=bot, user_id=call.from_user.id, json=json)

            else:
                flower_group_title = call.data.split(" ")[-2]
                flower_group_id = call.data.split(" ")[-1]
                json[str_user_id]['flower_group_title'] = flower_group_title
                json[str_user_id]['flower_group_id'] = flower_group_id
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_add_flower_ask_photo_message(bot=bot, user_id=call.from_user.id, json=json)

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('flower_adding_ask_photo'))
def add_flower_photo_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                flowers_groups = sql_alchemy.get_user_groups(call.from_user.id)
                MessageHandler.send_add_flower_group_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    flowers_groups=flowers_groups
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif 'yes' in call.data:
                json[str_user_id]['set_flower_photo'] = True
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_add_flower_photo_message(bot=bot, user_id=call.from_user.id, json=json)

            elif 'no' in call.data:
                with open('static/images/base_flower_photo.jpg', 'rb') as file:
                    photo = file.read()

                sql_alchemy.add_flower(
                    str_user_id=str_user_id,
                    json_data=json,
                    bytes_photo=pickle.dumps(photo)
                )

                MessageHandler.send_add_flower_created_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    bytes_photo=pickle.dumps(photo)
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

                MessageHandler.send_add_flower_ask_photo_message(bot=bot, user_id=call.from_user.id, json=json)

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('flower_adding_created'))
def add_flower_created_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'another' in call.data:
                json[str_user_id]['set_flower_title'] = True
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_add_flower_title_message(bot=bot, user_id=call.from_user.id, json=json)

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

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
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif 'add_flower' in call.data:
                json[str_user_id]['set_flower_title'] = True
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_add_flower_title_message(bot=bot, user_id=call.from_user.id, json=json)

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


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_action'))
def check_flower_action_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            flower_id = int(call.data.split(' ')[-1])
            flower = sql_alchemy.get_flower(flower_id)

            if 'BACK' in call.data:
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

            # TODO наверное, вынести куда-то отдельно в метод, ибо по кд вызывается в редактировании цветка
            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif 'change' in call.data:
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_flower_choose_changing_point_markup(
                        flower_id=flower_id
                    ),
                    media=InputMediaPhoto(
                        media=pickle.loads(flower.photo),
                        caption=TemplateCreator().check_flower_choose_changing_point(
                            flower_description=DatabaseParser.parse_flower(
                                sql_alchemy_adapter=sql_alchemy,
                                flower=flower
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif 'delete' in call.data:
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_flower_confirm_delete_markup(
                        flower_id=flower_id
                    ),
                    media=InputMediaPhoto(
                        media=pickle.loads(flower.photo),
                        caption=TemplateCreator().check_flower_confirm_delete(
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_confirm_delete'))
def check_flower_confirm_delete_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            flower_id = int(call.data.split(' ')[-1])
            flower = sql_alchemy.get_flower(flower_id)

            if 'NO' in call.data:
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

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif 'YES' in call.data:
                sql_alchemy.delete_flower(flower_id)
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_choose_changing_point'))
def check_flower_choose_changing_point_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()
            point_to_change = call.data.split(' ')[-2]

            flower_id = int(call.data.split(' ')[-1])
            flower = sql_alchemy.get_flower(flower_id)

            match point_to_change:
                case 'BACK':
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

                case "MENU":
                    JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                    MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

                case "title":
                    json[str_user_id]['set_flower_title'] = True
                    json[str_user_id]['refactor'] = True
                    json[str_user_id]['flower_id'] = flower_id
                    JsonHandler(json_name).write_json_data(json)

                    bot.edit_message_media(
                        chat_id=call.from_user.id,
                        message_id=json[str_user_id]['message_for_update'],
                        reply_markup=MarkupCreator().check_flower_change_markup(
                            flower_id=flower_id
                        ),
                        media=InputMediaPhoto(
                            media=pickle.loads(flower.photo),
                            caption=TemplateCreator().check_flower_change_title(
                                flower_description=DatabaseParser.parse_flower(
                                    sql_alchemy_adapter=sql_alchemy,
                                    flower=flower
                                )
                            ),
                            parse_mode='HTML'
                        )
                    )

                case "description":
                    json[str_user_id]['set_flower_description'] = True
                    json[str_user_id]['refactor'] = True
                    json[str_user_id]['flower_id'] = flower_id
                    JsonHandler(json_name).write_json_data(json)

                    bot.edit_message_media(
                        chat_id=call.from_user.id,
                        message_id=json[str_user_id]['message_for_update'],
                        reply_markup=MarkupCreator().check_flower_change_markup(
                            flower_id=flower_id
                        ),
                        media=InputMediaPhoto(
                            media=pickle.loads(flower.photo),
                            caption=TemplateCreator().check_flower_change_description(
                                flower_description=DatabaseParser.parse_flower(
                                    sql_alchemy_adapter=sql_alchemy,
                                    flower=flower
                                )
                            ),
                            parse_mode='HTML'
                        )
                    )

                case "photo":
                    json[str_user_id]['set_flower_photo'] = True
                    json[str_user_id]['refactor'] = True
                    json[str_user_id]['flower_id'] = flower_id
                    JsonHandler(json_name).write_json_data(json)

                    bot.edit_message_media(
                        chat_id=call.from_user.id,
                        message_id=json[str_user_id]['message_for_update'],
                        reply_markup=MarkupCreator().check_flower_change_markup(
                            flower_id=flower_id
                        ),
                        media=InputMediaPhoto(
                            media=pickle.loads(flower.photo),
                            caption=TemplateCreator().check_flower_change_photo(
                                flower_description=DatabaseParser.parse_flower(
                                    sql_alchemy_adapter=sql_alchemy,
                                    flower=flower
                                )
                            ),
                            parse_mode='HTML'
                        )
                    )

                case "group":
                    json[str_user_id]['flower_id'] = flower_id
                    JsonHandler(json_name).write_json_data(json)

                    user_groups = sql_alchemy.get_user_groups(call.from_user.id)

                    bot.edit_message_media(
                        chat_id=call.from_user.id,
                        message_id=json[str_user_id]['message_for_update'],
                        reply_markup=MarkupCreator().check_flower_change_group_markup(
                            flower_id=flower_id,
                            user_groups=user_groups
                        ),
                        media=InputMediaPhoto(
                            media=pickle.loads(flower.photo),
                            caption=TemplateCreator().check_flower_change_group(
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_change_group'))
def check_flower_change_group_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            flower_id = int(call.data.split(' ')[-1])
            flower = sql_alchemy.get_flower(flower_id)

            if 'BACK' in call.data:
                # TODO наверное, вынести куда-то отдельно в метод, ибо по кд вызывается в редактировании цветка
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_flower_choose_changing_point_markup(
                        flower_id=flower_id
                    ),
                    media=InputMediaPhoto(
                        media=pickle.loads(flower.photo),
                        caption=TemplateCreator().check_flower_choose_changing_point(
                            flower_description=DatabaseParser.parse_flower(
                                sql_alchemy_adapter=sql_alchemy,
                                flower=flower
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            else:
                group_id = call.data.split(' ')[-1]
                sql_alchemy.change_flower_group(
                    flower_id=json[str_user_id]['flower_id'],
                    new_group_id=group_id
                )

                # TODO можно тоже вынести в отдельный метод, ибо есть повторение ниже
                flower = sql_alchemy.get_flower(json[str_user_id]['flower_id'])

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_flower_choose_changing_point_markup(
                        flower_id=json[str_user_id]['flower_id']
                    ),
                    media=InputMediaPhoto(
                        media=pickle.loads(flower.photo),
                        caption=TemplateCreator().check_flower_choose_changing_point(
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_change'))
def check_flower_change_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            flower_id = int(call.data.split(' ')[-1])
            flower = sql_alchemy.get_flower(flower_id)

            if 'BACK' in call.data:
                # TODO наверное, вынести куда-то отдельно в метод, ибо по кд вызывается в редактировании цветка
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_flower_choose_changing_point_markup(
                        flower_id=flower_id
                    ),
                    media=InputMediaPhoto(
                        media=pickle.loads(flower.photo),
                        caption=TemplateCreator().check_flower_choose_changing_point(
                            flower_description=DatabaseParser.parse_flower(
                                sql_alchemy_adapter=sql_alchemy,
                                flower=flower
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

    except Exception as e:
        logger.error(e)


"""
    Ниже идет логика по просмотру, редактированию и удалению сценариев (групп) полива.
"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_groups'))
def check_groups_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            user_groups = sql_alchemy.get_user_groups(call.from_user.id)

            bot.edit_message_media(
                chat_id=call.from_user.id,
                message_id=json[str_user_id]['message_for_update'],
                reply_markup=MarkupCreator().check_group_selection_markup(
                    user_groups=user_groups
                ),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().check_group_selection(
                        empty_groups=True if len(user_groups) > 0 else False
                    ),
                    parse_mode='HTML'
                )
            )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_selection'))
def check_group_selection_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif 'add_group' in call.data:
                json[str_user_id]['set_group_title'] = True
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_add_group_title_message(bot=bot, user_id=call.from_user.id, json=json)

            else:
                group_id = int(call.data.split(' ')[-1])
                group = sql_alchemy.get_group(group_id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_action_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_action(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_action'))
def check_group_action_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            group_id = int(call.data.split(' ')[-1])
            group = sql_alchemy.get_group(group_id)

            if 'BACK' in call.data:
                user_groups = sql_alchemy.get_user_groups(call.from_user.id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_selection_markup(
                        user_groups=user_groups
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_selection(
                            empty_groups=True if len(user_groups) > 0 else False
                        ),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif 'change' in call.data:
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_choose_changing_point(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif 'delete' in call.data:
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_confirm_delete_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_confirm_delete(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif 'see_flowers':
                group_flowers = sql_alchemy.get_group_flowers(group_id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_see_flowers_markup(
                        group_flowers=group_flowers,
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_see_flowers(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_see_flowers'))
def check_group_see_flowers_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            group_id = int(call.data.split(' ')[-1])
            group = sql_alchemy.get_group(group_id)

            if 'BACK' in call.data:
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_action_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_action(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            else:
                flower_id = int(call.data.split(' ')[-2])
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


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_confirm_delete'))
def check_group_confirm_delete_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            group_id = int(call.data.split(' ')[-1])
            group = sql_alchemy.get_group(group_id)

            if 'NO' in call.data:
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_action_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_action(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif 'YES' in call.data:
                sql_alchemy.delete_group(group_id)

                user_groups = sql_alchemy.get_user_groups(call.from_user.id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_selection_markup(
                        user_groups=user_groups
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_selection(
                            empty_groups=True if len(user_groups) > 0 else False
                        ),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_choose_changing_point'))
def check_group_choose_changing_point_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()
            point_to_change = call.data.split(' ')[-2]

            group_id = int(call.data.split(' ')[-1])
            group = sql_alchemy.get_group(group_id)

            match point_to_change:
                case 'BACK':
                    bot.edit_message_media(
                        chat_id=call.from_user.id,
                        message_id=json[str_user_id]['message_for_update'],
                        reply_markup=MarkupCreator().check_group_action_markup(
                            group_id=group_id
                        ),
                        media=InputMediaPhoto(
                            media=open('static/images/media_message_picture.png', 'rb'),
                            caption=TemplateCreator().check_group_action(
                                group_description=DatabaseParser.parse_group(
                                    sql_alchemy_adapter=sql_alchemy,
                                    group=group
                                )
                            ),
                            parse_mode='HTML'
                        )
                    )

                case "MENU":
                    JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                    MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

                case "title":
                    json[str_user_id]['set_group_title'] = True
                    json[str_user_id]['refactor'] = True
                    json[str_user_id]['group_id'] = group_id
                    JsonHandler(json_name).write_json_data(json)

                    bot.edit_message_media(
                        chat_id=call.from_user.id,
                        message_id=json[str_user_id]['message_for_update'],
                        reply_markup=MarkupCreator().check_group_change_markup(
                            group_id=group_id
                        ),
                        media=InputMediaPhoto(
                            media=open('static/images/media_message_picture.png', 'rb'),
                            caption=TemplateCreator().check_group_change_title(
                                group_description=DatabaseParser.parse_group(
                                    sql_alchemy_adapter=sql_alchemy,
                                    group=group
                                )
                            ),
                            parse_mode='HTML'
                        )
                    )

                case "description":
                    json[str_user_id]['set_group_description'] = True
                    json[str_user_id]['refactor'] = True
                    json[str_user_id]['group_id'] = group_id
                    JsonHandler(json_name).write_json_data(json)

                    bot.edit_message_media(
                        chat_id=call.from_user.id,
                        message_id=json[str_user_id]['message_for_update'],
                        reply_markup=MarkupCreator().check_group_change_markup(
                            group_id=group_id
                        ),
                        media=InputMediaPhoto(
                            media=open('static/images/media_message_picture.png', 'rb'),
                            caption=TemplateCreator().check_group_change_description(
                                group_description=DatabaseParser.parse_group(
                                    sql_alchemy_adapter=sql_alchemy,
                                    group=group
                                )
                            ),
                            parse_mode='HTML'
                        )
                    )

                case "last_watering_date":
                    now = datetime.now()
                    json[str_user_id]['group_id'] = group_id
                    JsonHandler(json_name).write_json_data(json)

                    bot.edit_message_media(
                        chat_id=call.from_user.id,
                        message_id=json[str_user_id]['message_for_update'],
                        reply_markup=calendar.create_calendar(
                            name=change_group_calendar_callback.prefix,
                            year=now.year,
                            month=now.month
                        ),
                        media=InputMediaPhoto(
                            media=open('static/images/media_message_picture.png', 'rb'),
                            caption=TemplateCreator().check_group_change_last_watering_date(
                                group_description=DatabaseParser.parse_group(
                                    sql_alchemy_adapter=sql_alchemy,
                                    group=group
                                )
                            ),
                            parse_mode='HTML'
                        )
                    )

                case "watering_interval":
                    bot.edit_message_media(
                        chat_id=call.from_user.id,
                        message_id=json[str_user_id]['message_for_update'],
                        reply_markup=MarkupCreator().check_group_change_watering_interval_markup(
                            group_id=group_id
                        ),
                        media=InputMediaPhoto(
                            media=open('static/images/media_message_picture.png', 'rb'),
                            caption=TemplateCreator().check_group_change_watering_interval(
                                group_description=DatabaseParser.parse_group(
                                    sql_alchemy_adapter=sql_alchemy,
                                    group=group
                                )
                            ),
                            parse_mode='HTML'
                        )
                    )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_change_watering_interval'))
def check_group_change_watering_interval_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            group_id = int(call.data.split(' ')[-1])
            group = sql_alchemy.get_group(group_id)

            if 'BACK' in call.data:
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_choose_changing_point(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            else:
                new_watering_interval = int(call.data.split(' ')[-2])

                sql_alchemy.change_group_watering_interval(
                    group_id=group_id,
                    new_watering_interval=new_watering_interval
                )

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_choose_changing_point(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(change_group_calendar_callback.prefix))
def check_group_change_last_watering_date_call_query(call: CallbackQuery):
    try:
        if call.message:
            json = JsonHandler(json_name).read_json_file()
            str_user_id = str(call.from_user.id)

            group_id = json[str_user_id]['group_id']
            group = sql_alchemy.get_group(group_id)

            name, action, year, month, day = call.data.split(create_group_calendar_callback.sep)
            new_last_watering_date = calendar.calendar_query_handler(
                bot=bot,
                call=call,
                name=name,
                action=action,
                year=year,
                month=month,
                day=day
            )

            if action == "DAY":
                sql_alchemy.change_group_last_watering_date(
                    group_id=group_id,
                    new_last_watering_date=new_last_watering_date
                )

                group = sql_alchemy.get_group(group_id)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_choose_changing_point(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif action == "MENU":
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

            elif action == "BACK":
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_choose_changing_point(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_change'))
def check_group_change_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            group_id = int(call.data.split(' ')[-1])
            group = sql_alchemy.get_group(group_id)

            if 'BACK' in call.data:
                # TODO наверное, вынести куда-то отдельно в метод, ибо по кд вызывается в редактировании цветка
                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                        group_id=group_id
                    ),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().check_group_choose_changing_point(
                            group_description=DatabaseParser.parse_group(
                                sql_alchemy_adapter=sql_alchemy,
                                group=group
                            )
                        ),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)

    except Exception as e:
        logger.error(e)


"""
    Ниже идет логика по обработке сообщений от пользователей.
"""


@bot.message_handler(content_types= ['text'], func=lambda message: JsonHandler(
    json_name).check_refactor_status(str(message.from_user.id)) is False)
def create_item_text_messages_handler(message):
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

        MessageHandler.send_add_group_description_message(bot=bot, user_id=message.from_user.id, json=json)

    elif json[str_user_id]['set_group_description']:
        json[str_user_id]['set_group_description'] = False
        json[str_user_id]['group_description'] = message.text
        JsonHandler(json_name).write_json_data(json)

        # TODO вынести в метод базового Message_Handler
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        MessageHandler.send_add_group_last_watering_date_message(bot=bot, user_id=message.from_user.id, json=json)

    elif json[str_user_id]['set_flower_title']:
        json[str_user_id]['set_flower_title'] = False
        json[str_user_id]['set_flower_description'] = True
        json[str_user_id]['flower_title'] = message.text
        JsonHandler(json_name).write_json_data(json)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        MessageHandler.send_add_flower_description_message(bot=bot, user_id=message.from_user.id, json=json)

    elif json[str_user_id]['set_flower_description']:
        json[str_user_id]['set_flower_description'] = False
        json[str_user_id]['flower_description'] = message.text
        JsonHandler(json_name).write_json_data(json)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        flowers_groups = sql_alchemy.get_user_groups(message.from_user.id)
        MessageHandler.send_add_flower_group_message(
            bot=bot,
            user_id=message.from_user.id,
            json=json,
            flowers_groups=flowers_groups
        )

    else:
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )


@bot.message_handler(content_types= ['photo'], func=lambda message: JsonHandler(
    json_name).check_refactor_status(str(message.from_user.id)) is False)
def create_item_photo_messages_handler(message):
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

        MessageHandler.send_add_flower_created_message(
            bot=bot,
            user_id=message.from_user.id,
            json=json,
            bytes_photo=bytes_photo
        )

    else:
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )


@bot.message_handler(content_types= ['text'], func=lambda message: JsonHandler(
    json_name).check_refactor_status(str(message.from_user.id)) is True)
def change_item_text_messages_handler(message):
    str_user_id = str(message.from_user.id)
    json = JsonHandler(json_name).read_json_file()

    if json.get(str_user_id, None) is None:
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        return

    if json[str_user_id]['set_group_title']:
        json[str_user_id]['group_title'] = message.text
        JsonHandler(json_name).write_json_data(json)
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        sql_alchemy.change_group_title(
            group_id=json[str_user_id]['group_id'],
            new_title=json[str_user_id]['group_title']
        )

        # TODO можно тоже вынести в отдельный метод, ибо есть повторение ниже
        group = sql_alchemy.get_group(json[str_user_id]['group_id'])

        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                group_id=json[str_user_id]['group_id']
            ),
            media=InputMediaPhoto(
                media=open('static/images/media_message_picture.png', 'rb'),
                caption=TemplateCreator().check_group_choose_changing_point(
                    group_description=DatabaseParser.parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )

    elif json[str_user_id]['set_group_description']:
        json[str_user_id]['group_description'] = message.text
        JsonHandler(json_name).write_json_data(json)
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        sql_alchemy.change_group_description(
            group_id=json[str_user_id]['group_id'],
            new_description=json[str_user_id]['group_description']
        )

        # TODO можно тоже вынести в отдельный метод, ибо есть повторение ниже
        group = sql_alchemy.get_group(json[str_user_id]['group_id'])

        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=MarkupCreator().check_group_choose_changing_point_markup(
                group_id=json[str_user_id]['group_id']
            ),
            media=InputMediaPhoto(
                media=open('static/images/media_message_picture.png', 'rb'),
                caption=TemplateCreator().check_group_choose_changing_point(
                    group_description=DatabaseParser.parse_group(
                        sql_alchemy_adapter=sql_alchemy,
                        group=group
                    )
                ),
                parse_mode='HTML'
            )
        )

    elif json[str_user_id]['set_flower_title']:
        json[str_user_id]['flower_title'] = message.text
        JsonHandler(json_name).write_json_data(json)
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        sql_alchemy.change_flower_title(
            flower_id=json[str_user_id]['flower_id'],
            new_title=json[str_user_id]['flower_title']
        )

        # TODO можно тоже вынести в отдельный метод, ибо есть повторение ниже
        flower = sql_alchemy.get_flower(json[str_user_id]['flower_id'])

        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_choose_changing_point_markup(
                flower_id=json[str_user_id]['flower_id']
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_choose_changing_point(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
                ),
                parse_mode='HTML'
            )
        )


    elif json[str_user_id]['set_flower_description']:
        json[str_user_id]['flower_description'] = message.text
        JsonHandler(json_name).write_json_data(json)
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        sql_alchemy.change_flower_description(
            flower_id=json[str_user_id]['flower_id'],
            new_description=json[str_user_id]['flower_description']
        )

        flower = sql_alchemy.get_flower(json[str_user_id]['flower_id'])

        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_choose_changing_point_markup(
                flower_id=json[str_user_id]['flower_id']
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_choose_changing_point(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
                ),
                parse_mode='HTML'
            )
        )

    else:
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )


@bot.message_handler(content_types= ['photo'], func=lambda message: JsonHandler(
    json_name).check_refactor_status(str(message.from_user.id)) is True)
def change_item_photo_messages_handler(message):
    str_user_id = str(message.from_user.id)
    json = JsonHandler(json_name).read_json_file()

    if json.get(str_user_id, None) is None:
        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        return

    if json[str_user_id]['set_flower_photo']:
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        photo = bot.get_file(message.photo[-1].file_id)
        bytes_photo = PhotoProcessor.get_photo_from_message(photo)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        sql_alchemy.change_flower_photo(
            flower_id=json[str_user_id]['flower_id'],
            new_bytes_photo=bytes_photo
        )

        flower = sql_alchemy.get_flower(json[str_user_id]['flower_id'])

        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=MarkupCreator().check_flower_choose_changing_point_markup(
                flower_id=json[str_user_id]['flower_id']
            ),
            media=InputMediaPhoto(
                media=pickle.loads(flower.photo),
                caption=TemplateCreator().check_flower_choose_changing_point(
                    flower_description=DatabaseParser.parse_flower(
                        sql_alchemy_adapter=sql_alchemy,
                        flower=flower
                    )
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
