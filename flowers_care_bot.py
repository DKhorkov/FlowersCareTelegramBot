import telebot
from datetime import timedelta, datetime

import settings
from db_commands import DataBase

bot = telebot.TeleBot(settings.TOKEN)
URL = "https://api.telegram.org/bot{}/".format(settings.TOKEN)
db = DataBase()
db.create_database()


@bot.message_handler(commands=['help'])
def help_instruction(message):
    instruction = """Чтобы начать пользоваться ботом, введите команду /start.
    \nДля того, чтобы начать отслеживать время полива растения, нажмите на кнопку "🌷 Добавить растение".
    \nЧтобы посмотреть статус полива растений, введите команду /watering_status."""
    bot.send_message(message.chat.id, instruction)


@bot.message_handler(commands=['start'])
def start(message):
    sticker = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    # keyboard
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("🌷 Добавить растение")
    markup.add(item1)

    # Adding user to a database if he is not already in it:
    data = db.check_if_user_is_already_in_database(message.chat.id)
    if data is None:
        db.add_user_to_database(message)
    else:
        print('This user is already exists')

    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name}, добро пожаловать в {bot.get_me().username}! '
                     f'Здесь вы можете добавить свое растение, чтобы бот отправлял вам уведомление,'
                     f' когда его необходимо полить!', parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['watering_status'])
def watering_status(message):
    users_flowers = db.selecting_flowers_from_database(message.chat.id)
    answer = 'Статус полива ваших цветов:'
    mark = 1
    for flower in users_flowers:
        watering_time = datetime.strptime(flower[4], "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=flower[3])
        current_time = datetime.now()
        if watering_time <= current_time:
            msg = f'\n{mark}) Необходимо было полить цветок {flower[1]} типа {flower[2]} {watering_time}.'
            mark += 1
            answer += msg
        else:
            msg = f'\n{mark}) Необходимо будет полить цветок {flower[1]} типа {flower[2]} ' \
                  f'в следующий раз {watering_time}.'
            mark += 1
            answer += msg
    bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=['text'])
def user_message(message):
    if message.chat.type == 'private':
        if message.text == "🌷 Добавить растение":
            bot.send_message(message.chat.id, "Пожалуйста, введите название растения:")
            bot.register_next_step_handler(message, get_flower_name)

        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢'
                                              '\nДля получения информации о возможностях бота введите команду "/help".')


users_dict = {}


def get_flower_name(message):
    users_dict[message.chat.id] = [message.text]
    bot.send_message(message.chat.id,  "Пожалуйста, введите тип растения:")
    bot.register_next_step_handler(message, get_flower_type)


def get_flower_type(message):
    flower_info_list = users_dict[message.chat.id]
    flower_info_list.append(message.text)
    users_dict[message.chat.id] = flower_info_list
    bot.send_message(message.chat.id, "Пожалуйста, введите интервал полива растения в часах:")
    bot.register_next_step_handler(message, get_flower_watering_interval)


def get_flower_watering_interval(message):
    try:
        int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели информацию некорректно, пожалуйста, введите цифрами целое число:')
        bot.register_next_step_handler(message, get_flower_watering_interval)
    else:
        flower_info_list = users_dict[message.chat.id]
        flower_info_list.append(message.text)
        users_dict[message.chat.id] = flower_info_list
        keyboard = telebot.types.InlineKeyboardMarkup()
        key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes')
        key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no, key_yes)
        question = f'Проверим инфу: цветок {users_dict[message.chat.id][0]} типа {users_dict[message.chat.id][1]},' \
                   f'который необходимо поливать каждые {users_dict[message.chat.id][2]} часов?'
        bot.send_message(message.chat.id, question, reply_markup=keyboard)


# Обработчик ответа на клавиатуре пользователя на вопрос, правильно ли введена инфа про цветок:
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        current_time = datetime.now()
        db.add_flower_info_to_database(call.message.chat.id, users_dict[call.message.chat.id][0],
                                       users_dict[call.message.chat.id][1], users_dict[call.message.chat.id][2],
                                       current_time)

        # Remove inline buttons and send notification:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Растение сохранено. Ждите уведомления о необходимости полива!)", reply_markup=None)
    elif call.data == "no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Начните с начала!)", reply_markup=None)


bot.polling(none_stop=True)
