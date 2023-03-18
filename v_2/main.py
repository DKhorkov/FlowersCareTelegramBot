import pickle

from telebot import TeleBot
from telebot_calendar import CallbackData, RUSSIAN_LANGUAGE
from telebot.types import CallbackQuery, Message

from v_2.configs import TOKEN, json_name
from v_2.helpers.logging_system import get_logger
from v_2.helpers.customized_calendar import CustomizedCalendar
from v_2.helpers.json_handler import JsonHandler
from v_2.helpers.photo_processor import PhotoProcessor
from v_2.helpers.message_handlers.main_message_handler import MessageHandler
from v_2.helpers.sql_alchemy.adapter import SQLAlchemyAdapter


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
def start(message: Message) -> None:
    if sql_alchemy.check_if_user_already_registered(message.from_user.id):
        sql_alchemy.add_user(message)
        #TODO Добавить приветственное сообщение с отправкой инфы по боту и его командам. Создать команду --help

    message_for_update = MessageHandler.send_start_message(bot=bot, message=message)
    JsonHandler(json_name).prepare_json(user_id=message.from_user.id, message_for_update=message_for_update)


"""
    Ниже идет логика по созданию сценария (группы) полива цветов.
"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_group'))
def add_group_call_query(call: CallbackQuery) -> None:
    try:
        str_user_id = str(call.from_user.id)
        json = JsonHandler(json_name).read_json_file()
        json[str_user_id]['set_group_title'] = True
        JsonHandler(json_name).write_json_data(json)

        MessageHandler.send_add_group_title_message(bot=bot, user_id=call.from_user.id, json=json)
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_title'))
def add_group_title_call_query(call: CallbackQuery) -> None:
    try:
        str_user_id = str(call.from_user.id)
        json = JsonHandler(json_name).read_json_file()
        if 'BACK' in call.data:
            json[str_user_id]['set_group_title'] = False
            JsonHandler(json_name).write_json_data(json)

            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_description'))
def add_group_description_call_query(call: CallbackQuery) -> None:
    try:
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
def add_group_last_watering_date_call_query(call: CallbackQuery) -> None:
    try:
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
def add_group_watering_interval_call_query(call: CallbackQuery) -> None:
    try:
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
def add_group_created_call_query(call: CallbackQuery) -> None:
    try:
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
def back_to_menu_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
    except Exception as e:
        logger.error(e)


"""
    Ниже идет логика по добавлению цветков.
"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_flower'))
def add_flower_call_query(call: CallbackQuery) -> None:
    try:
        str_user_id = str(call.from_user.id)
        json = JsonHandler(json_name).read_json_file()
        json[str_user_id]['set_flower_title'] = True
        JsonHandler(json_name).write_json_data(json)

        MessageHandler.send_add_flower_title_message(bot=bot, user_id=call.from_user.id, json=json)
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('flower_adding_title'))
def add_flower_title_call_query(call: CallbackQuery) -> None:
    try:
        str_user_id = str(call.from_user.id)
        json = JsonHandler(json_name).read_json_file()
        if 'BACK' in call.data:
            json[str_user_id]['set_flower_title'] = False
            JsonHandler(json_name).write_json_data(json)

            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('flower_adding_description'))
def add_flower_description_call_query(call: CallbackQuery) -> None:
    try:
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
def add_flower_group_call_query(call: CallbackQuery) -> None:
    try:
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
def add_flower_photo_call_query(call: CallbackQuery) -> None:
    try:
        str_user_id = str(call.from_user.id)
        json = JsonHandler(json_name).read_json_file()
        if 'BACK' in call.data:
            MessageHandler.send_add_flower_group_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                flowers_groups=sql_alchemy.get_user_groups(call.from_user.id)
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str_user_id)
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
        elif 'yes' in call.data:
            json[str_user_id]['set_flower_photo'] = True
            JsonHandler(json_name).write_json_data(json)

            MessageHandler.send_add_flower_photo_message(bot=bot, user_id=call.from_user.id, json=json)
        elif 'no' in call.data:
            with open('helpers/static/images/base_flower_photo.jpg', 'rb') as file:
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
def add_flower_photo_call_query(call: CallbackQuery) -> None:
    try:
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
def add_flower_created_call_query(call: CallbackQuery) -> None:
    try:
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
def check_flowers_call_query(call: CallbackQuery) -> None:
    try:
        MessageHandler.send_check_flower_selection_message(
            bot=bot,
            user_id=call.from_user.id,
            json=JsonHandler(json_name).read_json_file(),
            user_flowers=sql_alchemy.get_user_flowers(call.from_user.id)
        )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_selection'))
def check_flower_selection_call_query(call: CallbackQuery) -> None:
    try:
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
            MessageHandler.send_check_flower_action_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                flower=sql_alchemy.get_flower(flower_id),
                flower_id=flower_id,
                sql_alchemy=sql_alchemy
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_action'))
def check_flower_action_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        flower_id = int(call.data.split(' ')[-1])
        flower = sql_alchemy.get_flower(flower_id)
        if 'BACK' in call.data:
            MessageHandler.send_check_flower_selection_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                user_flowers=sql_alchemy.get_user_flowers(call.from_user.id)
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str(call.from_user.id))
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
        elif 'change' in call.data:
            MessageHandler.send_check_flower_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                flower=flower,
                flower_id=flower_id,
                sql_alchemy=sql_alchemy
            )
        elif 'delete' in call.data:
            MessageHandler.send_check_flower_confirm_delete_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                flower=flower,
                flower_id=flower_id,
                sql_alchemy=sql_alchemy
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_confirm_delete'))
def check_flower_confirm_delete_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        flower_id = int(call.data.split(' ')[-1])
        flower = sql_alchemy.get_flower(flower_id)
        if 'NO' in call.data:
            MessageHandler.send_check_flower_action_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                flower=flower,
                flower_id=flower_id,
                sql_alchemy=sql_alchemy
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str(call.from_user.id))
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
        elif 'YES' in call.data:
            sql_alchemy.delete_flower(flower_id)
            MessageHandler.send_check_flower_selection_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                user_flowers=sql_alchemy.get_user_flowers(call.from_user.id)
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_choose_changing_point'))
def check_flower_choose_changing_point_call_query(call: CallbackQuery) -> None:
    try:
        str_user_id = str(call.from_user.id)
        json = JsonHandler(json_name).read_json_file()

        point_to_change = call.data.split(' ')[-2]
        flower_id = int(call.data.split(' ')[-1])
        flower = sql_alchemy.get_flower(flower_id)
        match point_to_change:
            case 'BACK':
                MessageHandler.send_check_flower_action_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    flower=flower,
                    flower_id=flower_id,
                    sql_alchemy=sql_alchemy
                )
            case "MENU":
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
            case "title":
                json[str_user_id]['set_flower_title'] = True
                json[str_user_id]['refactor'] = True
                json[str_user_id]['flower_id'] = flower_id
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_check_flower_change_title_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    flower=flower,
                    flower_id=flower_id,
                    sql_alchemy=sql_alchemy
                )
            case "description":
                json[str_user_id]['set_flower_description'] = True
                json[str_user_id]['refactor'] = True
                json[str_user_id]['flower_id'] = flower_id
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_check_flower_change_description_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    flower=flower,
                    flower_id=flower_id,
                    sql_alchemy=sql_alchemy
                )
            case "photo":
                json[str_user_id]['set_flower_photo'] = True
                json[str_user_id]['refactor'] = True
                json[str_user_id]['flower_id'] = flower_id
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_check_flower_change_photo_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    flower=flower,
                    flower_id=flower_id,
                    sql_alchemy=sql_alchemy
                )
            case "group":
                json[str_user_id]['flower_id'] = flower_id
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_check_flower_change_group_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    flower=flower,
                    flower_id=flower_id,
                    sql_alchemy=sql_alchemy,
                    user_groups=sql_alchemy.get_user_groups(call.from_user.id)
                )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_change_group'))
def check_flower_change_group_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        flower_id = int(call.data.split(' ')[-1])
        flower = sql_alchemy.get_flower(flower_id)
        if 'BACK' in call.data:
            MessageHandler.send_check_flower_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                flower=flower,
                flower_id=flower_id,
                sql_alchemy=sql_alchemy
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str(call.from_user.id))
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
        else:
            group_id = int(call.data.split(' ')[-1])
            sql_alchemy.change_flower_group(
                flower_id=flower_id,
                new_group_id=group_id
            )

            MessageHandler.send_check_flower_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                flower=sql_alchemy.get_flower(flower_id),
                flower_id=flower_id,
                sql_alchemy=sql_alchemy
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_flower_change'))
def check_flower_change_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        flower_id = int(call.data.split(' ')[-1])
        flower = sql_alchemy.get_flower(flower_id)
        if 'BACK' in call.data:
            MessageHandler.send_check_flower_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                flower=flower,
                flower_id=flower_id,
                sql_alchemy=sql_alchemy
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str(call.from_user.id))
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
    except Exception as e:
        logger.error(e)


"""
    Ниже идет логика по просмотру, редактированию и удалению сценариев (групп) полива.
"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_groups'))
def check_groups_call_query(call: CallbackQuery) -> None:
    try:
        MessageHandler.send_check_group_selection_message(
            bot=bot,
            user_id=call.from_user.id,
            json=JsonHandler(json_name).read_json_file(),
            user_groups=sql_alchemy.get_user_groups(call.from_user.id)
        )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_selection'))
def check_group_selection_call_query(call: CallbackQuery) -> None:
    try:
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
            MessageHandler.send_check_group_action_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=sql_alchemy.get_group(group_id),
                sql_alchemy=sql_alchemy
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_action'))
def check_group_action_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        group_id = int(call.data.split(' ')[-1])
        group = sql_alchemy.get_group(group_id)
        if 'BACK' in call.data:
            user_groups = sql_alchemy.get_user_groups(call.from_user.id)
            MessageHandler.send_check_group_selection_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                user_groups=user_groups
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str(call.from_user.id))
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
        elif 'change' in call.data:
            MessageHandler.send_check_group_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=group,
                sql_alchemy=sql_alchemy
            )
        elif 'delete' in call.data:
            MessageHandler.send_check_group_confirm_delete_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=group,
                sql_alchemy=sql_alchemy
            )
        elif 'see_flowers':
            MessageHandler.send_check_group_see_flowers_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=group,
                sql_alchemy=sql_alchemy,
                group_flowers=sql_alchemy.get_group_flowers(group_id)
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_see_flowers'))
def check_group_see_flowers_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        group_id = int(call.data.split(' ')[-1])
        group = sql_alchemy.get_group(group_id)
        if 'BACK' in call.data:
            MessageHandler.send_check_group_action_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=group,
                sql_alchemy=sql_alchemy
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str(call.from_user.id))
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
        else:
            flower_id = int(call.data.split(' ')[-2])
            flower = sql_alchemy.get_flower(flower_id)
            MessageHandler.send_check_flower_action_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                flower=flower,
                flower_id=flower_id,
                sql_alchemy=sql_alchemy
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_confirm_delete'))
def check_group_confirm_delete_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        group_id = int(call.data.split(' ')[-1])
        if 'NO' in call.data:
            MessageHandler.send_check_group_action_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=sql_alchemy.get_group(group_id),
                sql_alchemy=sql_alchemy
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str(call.from_user.id))
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
        elif 'YES' in call.data:
            sql_alchemy.delete_group(group_id)
            MessageHandler.send_check_group_selection_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                user_groups=sql_alchemy.get_user_groups(call.from_user.id)
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_choose_changing_point'))
def check_group_choose_changing_point_call_query(call: CallbackQuery) -> None:
    try:
        str_user_id = str(call.from_user.id)
        json = JsonHandler(json_name).read_json_file()
        point_to_change = call.data.split(' ')[-2]

        group_id = int(call.data.split(' ')[-1])
        group = sql_alchemy.get_group(group_id)
        match point_to_change:
            case 'BACK':
                MessageHandler.send_check_group_action_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    group_id=group_id,
                    group=group,
                    sql_alchemy=sql_alchemy
                )
            case "MENU":
                JsonHandler(json_name).reset_appropriate_messages(str_user_id)
                MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
            case "title":
                json[str_user_id]['set_group_title'] = True
                json[str_user_id]['refactor'] = True
                json[str_user_id]['group_id'] = group_id
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_check_group_change_title_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    group_id=group_id,
                    group=group,
                    sql_alchemy=sql_alchemy
                )
            case "description":
                json[str_user_id]['set_group_description'] = True
                json[str_user_id]['refactor'] = True
                json[str_user_id]['group_id'] = group_id
                JsonHandler(json_name).write_json_data(json)

                MessageHandler.send_check_group_change_description_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    group_id=group_id,
                    group=group,
                    sql_alchemy=sql_alchemy
                )
            case "last_watering_date":
                MessageHandler.send_check_group_change_last_watering_date_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    group=group,
                    sql_alchemy=sql_alchemy
                )
            case "watering_interval":
                MessageHandler.send_check_group_change_watering_interval_message(
                    bot=bot,
                    user_id=call.from_user.id,
                    json=json,
                    group_id=group_id,
                    group=group,
                    sql_alchemy=sql_alchemy
                )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_change_watering_interval'))
def check_group_change_watering_interval_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        group_id = int(call.data.split(' ')[-1])
        group = sql_alchemy.get_group(group_id)
        if 'BACK' in call.data:
            MessageHandler.send_check_group_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=group,
                sql_alchemy=sql_alchemy
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str(call.from_user.id))
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
        else:
            new_watering_interval = int(call.data.split(' ')[-2])

            sql_alchemy.change_group_watering_interval(
                group_id=group_id,
                new_watering_interval=new_watering_interval
            )

            MessageHandler.send_check_group_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=group,
                sql_alchemy=sql_alchemy
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith(change_group_calendar_callback.prefix))
def check_group_change_last_watering_date_call_query(call: CallbackQuery) -> None:
    try:
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

            MessageHandler.send_check_group_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=group,
                sql_alchemy=sql_alchemy
            )
        elif action == "MENU":
            JsonHandler(json_name).reset_appropriate_messages(str_user_id)
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
        elif action == "BACK":
            MessageHandler.send_check_group_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=group,
                sql_alchemy=sql_alchemy
            )
    except Exception as e:
        logger.error(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('check_group_change'))
def check_group_change_call_query(call: CallbackQuery) -> None:
    try:
        json = JsonHandler(json_name).read_json_file()
        group_id = int(call.data.split(' ')[-1])
        if 'BACK' in call.data:
            MessageHandler.send_check_group_choose_changing_point_message(
                bot=bot,
                user_id=call.from_user.id,
                json=json,
                group_id=group_id,
                group=sql_alchemy.get_group(group_id),
                sql_alchemy=sql_alchemy
            )
        elif "MENU" in call.data:
            JsonHandler(json_name).reset_appropriate_messages(str(call.from_user.id))
            MessageHandler.send_back_to_menu_message(bot=bot, user_id=call.from_user.id, json=json)
    except Exception as e:
        logger.error(e)


"""
    Ниже идет логика по обработке сообщений от пользователей.
"""


@bot.message_handler(content_types= ['text'], func=lambda message: JsonHandler(
    json_name).check_refactor_status(str(message.from_user.id)) is False)
def create_item_text_messages_handler(message: Message) -> None:
    str_user_id = str(message.from_user.id)
    json = JsonHandler(json_name).read_json_file()

    if json.get(str_user_id, None) is None:
        return MessageHandler.delete_message(bot=bot, message=message)
    if json[str_user_id]['set_group_title']:
        json[str_user_id]['set_group_title'] = False
        json[str_user_id]['set_group_description'] = True
        json[str_user_id]['group_title'] = message.text
        JsonHandler(json_name).write_json_data(json)

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_add_group_description_message(bot=bot, user_id=message.from_user.id, json=json)
    elif json[str_user_id]['set_group_description']:
        json[str_user_id]['set_group_description'] = False
        json[str_user_id]['group_description'] = message.text
        JsonHandler(json_name).write_json_data(json)

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_add_group_last_watering_date_message(bot=bot, user_id=message.from_user.id, json=json)
    elif json[str_user_id]['set_flower_title']:
        json[str_user_id]['set_flower_title'] = False
        json[str_user_id]['set_flower_description'] = True
        json[str_user_id]['flower_title'] = message.text
        JsonHandler(json_name).write_json_data(json)

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_add_flower_description_message(bot=bot, user_id=message.from_user.id, json=json)
    elif json[str_user_id]['set_flower_description']:
        json[str_user_id]['set_flower_description'] = False
        json[str_user_id]['flower_description'] = message.text
        JsonHandler(json_name).write_json_data(json)

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_add_flower_group_message(
            bot=bot,
            user_id=message.from_user.id,
            json=json,
            flowers_groups=sql_alchemy.get_user_groups(message.from_user.id)
        )
    else:
        MessageHandler.delete_message(bot=bot, message=message)


@bot.message_handler(content_types= ['photo'], func=lambda message: JsonHandler(
    json_name).check_refactor_status(str(message.from_user.id)) is False)
def create_item_photo_messages_handler(message: Message) -> None:
    str_user_id = str(message.from_user.id)
    json = JsonHandler(json_name).read_json_file()

    if json.get(str_user_id, None) is None:
        return MessageHandler.delete_message(bot=bot, message=message)

    if json[str_user_id]['set_flower_photo']:
        json[str_user_id]['set_flower_photo'] = False
        JsonHandler(json_name).write_json_data(json)

        photo = bot.get_file(message.photo[-1].file_id)
        bytes_photo = PhotoProcessor.get_photo_from_message(photo)

        sql_alchemy.add_flower(
            str_user_id=str_user_id,
            json_data=json,
            bytes_photo=bytes_photo
        )

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_add_flower_created_message(
            bot=bot,
            user_id=message.from_user.id,
            json=json,
            bytes_photo=bytes_photo
        )
    else:
        MessageHandler.delete_message(bot=bot, message=message)


@bot.message_handler(content_types= ['text'], func=lambda message: JsonHandler(
    json_name).check_refactor_status(str(message.from_user.id)) is True)
def change_item_text_messages_handler(message: Message) -> None:
    str_user_id = str(message.from_user.id)
    json = JsonHandler(json_name).read_json_file()

    if json.get(str_user_id, None) is None:
        return MessageHandler.delete_message(bot=bot, message=message)

    if json[str_user_id]['set_group_title']:
        group_id = json[str_user_id]['group_id']

        json[str_user_id]['group_title'] = message.text
        JsonHandler(json_name).write_json_data(json)
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        sql_alchemy.change_group_title(
            group_id=group_id,
            new_title=json[str_user_id]['group_title']
        )

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_check_group_choose_changing_point_message(
            bot=bot,
            user_id=message.from_user.id,
            json=json,
            group_id=group_id,
            group=sql_alchemy.get_group(group_id),
            sql_alchemy=sql_alchemy
        )
    elif json[str_user_id]['set_group_description']:
        group_id = json[str_user_id]['group_id']

        json[str_user_id]['group_description'] = message.text
        JsonHandler(json_name).write_json_data(json)
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        sql_alchemy.change_group_description(
            group_id=group_id,
            new_description=json[str_user_id]['group_description']
        )

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_check_group_choose_changing_point_message(
            bot=bot,
            user_id=message.from_user.id,
            json=json,
            group_id=group_id,
            group=sql_alchemy.get_group(group_id),
            sql_alchemy=sql_alchemy
        )
    elif json[str_user_id]['set_flower_title']:
        flower_id = json[str_user_id]['flower_id']

        json[str_user_id]['flower_title'] = message.text
        JsonHandler(json_name).write_json_data(json)
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        sql_alchemy.change_flower_title(
            flower_id=flower_id,
            new_title=json[str_user_id]['flower_title']
        )

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_check_flower_choose_changing_point_message(
            bot=bot,
            user_id=message.from_user.id,
            json=json,
            flower=sql_alchemy.get_flower(flower_id),
            flower_id=flower_id,
            sql_alchemy=sql_alchemy
        )
    elif json[str_user_id]['set_flower_description']:
        flower_id = json[str_user_id]['flower_id']

        json[str_user_id]['flower_description'] = message.text
        JsonHandler(json_name).write_json_data(json)
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        sql_alchemy.change_flower_description(
            flower_id=flower_id,
            new_description=json[str_user_id]['flower_description']
        )

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_check_flower_choose_changing_point_message(
            bot=bot,
            user_id=message.from_user.id,
            json=json,
            flower=sql_alchemy.get_flower(flower_id),
            flower_id=flower_id,
            sql_alchemy=sql_alchemy
        )
    else:
        MessageHandler.delete_message(bot=bot, message=message)


@bot.message_handler(content_types= ['photo'], func=lambda message: JsonHandler(
    json_name).check_refactor_status(str(message.from_user.id)) is True)
def change_item_photo_messages_handler(message: Message) -> None:
    str_user_id = str(message.from_user.id)
    json = JsonHandler(json_name).read_json_file()

    if json.get(str_user_id, None) is None:
        return MessageHandler.delete_message(bot=bot, message=message)

    if json[str_user_id]['set_flower_photo']:
        flower_id = json[str_user_id]['flower_id']
        JsonHandler(json_name).reset_appropriate_messages(str_user_id)

        photo = bot.get_file(message.photo[-1].file_id)
        bytes_photo = PhotoProcessor.get_photo_from_message(photo)

        sql_alchemy.change_flower_photo(
            flower_id=flower_id,
            new_bytes_photo=bytes_photo
        )

        MessageHandler.delete_message(bot=bot, message=message)
        MessageHandler.send_check_flower_choose_changing_point_message(
            bot=bot,
            user_id=message.from_user.id,
            json=json,
            flower=sql_alchemy.get_flower(flower_id),
            flower_id=flower_id,
            sql_alchemy=sql_alchemy
        )
    else:
        MessageHandler.delete_message(bot=bot, message=message)


@bot.message_handler(content_types= ['document', 'audio', 'video', 'sticker', 'video_note',
                                     'voice', 'location', 'contact'])
def dump_messages_handler(message: Message) -> None:
    MessageHandler.delete_message(bot=bot, message=message)


if __name__ == '__main__':
    bot.infinity_polling(timeout=100)
