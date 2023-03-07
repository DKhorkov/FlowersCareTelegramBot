from telebot import TeleBot
from telebot.types import InputMediaPhoto
from datetime import datetime

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


logger = get_logger('bot_logs')
bot = TeleBot(token=TOKEN)
json_name = 'users_data_json'
calendar = CustomizedCalendar(language=RUSSIAN_LANGUAGE)
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")


@bot.message_handler(commands=["start"])
def start(message):

    # TODO Добавить сохранения данных пользователя в таблицу БД, если юзер еще не подписан
    logger.info(f'User {message.from_user.id} have subscribed!')

    sticker = open('static/stickers/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)

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
        reply_markup=MarkupCreator().create_base_markup()
    )

    json_data[str_user_id] = {}
    json_data[str_user_id]['message_for_update'] = message_to_update
    JsonHandler(json_name).write_json_data(json_data)
    JsonHandler(json_name).reset_appropriate_messages(str_user_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_group'))
def creating_group_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()
            json[str_user_id]['set_group_name'] = True
            JsonHandler(json_name).write_json_data(json)

            bot.edit_message_media(
                chat_id=call.from_user.id,
                message_id=json[str_user_id]['message_for_update'],
                reply_markup=MarkupCreator().create_add_group_name_markup(),
                media=InputMediaPhoto(
                    media=open('static/images/media_message_picture.png', 'rb'),
                    caption=TemplateCreator().add_group_name(),
                    parse_mode='HTML'
                )
            )

    except Exception as e:
        logger.info(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_name'))
def add_group_name_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                json[str_user_id]['set_group_name'] = False
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().create_base_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().base_template(),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.info(e)


@bot.callback_query_handler(func=lambda call: call.data.startswith('group_adding_description'))
def add_group_description_call_query(call):
    try:
        if call.message:
            str_user_id = str(call.from_user.id)
            json = JsonHandler(json_name).read_json_file()

            if 'BACK' in call.data:
                json[str_user_id]['set_group_name'] = True
                json[str_user_id]['set_group_description'] = False
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().create_add_group_name_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().add_group_name(),
                        parse_mode='HTML'
                    )
                )

            elif "MENU" in call.data:
                json[str_user_id]['set_group_name'] = False
                json[str_user_id]['set_group_description'] = False
                JsonHandler(json_name).write_json_data(json)

                bot.edit_message_media(
                    chat_id=call.from_user.id,
                    message_id=json[str_user_id]['message_for_update'],
                    reply_markup=MarkupCreator().create_base_markup(),
                    media=InputMediaPhoto(
                        media=open('static/images/media_message_picture.png', 'rb'),
                        caption=TemplateCreator().base_template(),
                        parse_mode='HTML'
                    )
                )

    except Exception as e:
        logger.info(e)


@bot.message_handler(content_types= ['text'])
def text_messages_handler(message):
    str_user_id = str(message.from_user.id)
    json = JsonHandler(json_name).read_json_file()

    if json[str_user_id]['set_group_name']:
        json[str_user_id]['set_group_name'] = False
        json[str_user_id]['set_group_description'] = True
        json[str_user_id]['group_name'] = message.text
        JsonHandler(json_name).write_json_data(json)

        bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.id
        )

        bot.edit_message_media(
            chat_id=message.from_user.id,
            message_id=json[str_user_id]['message_for_update'],
            reply_markup=MarkupCreator().create_add_group_description_markup(),
            media=InputMediaPhoto(
                media=open('static/images/media_message_picture.png', 'rb'),
                caption=TemplateCreator().add_group_description(),
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
                caption=TemplateCreator().add_group_watering_last_time(),
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
