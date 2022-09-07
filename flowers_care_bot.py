import sqlite3
import telebot

import settings


bot = telebot.TeleBot(settings.TOKEN)
URL = "https://api.telegram.org/bot{}/".format(settings.TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    sticker = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    # keyboard
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("🌷 Добавить цветок")
    markup.add(item1)

    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name}, добро пожаловать в {bot.get_me().username}! '
                     f'Здесь вы можете добавить свой цветок, чтобы бот отправлял вам уведомление,'
                     f' когда его необходимо полить!', parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def user_message(message):
    if message.chat.type == 'private':
        if message.text == "🌷 Добавить цветок":
            bot.send_message(message.chat.id, "Добавляем цветок в БД")
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


bot.polling(none_stop=True)
