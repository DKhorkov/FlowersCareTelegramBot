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
    \nДля того, чтобы перестать отслеживать время полива растения, нажмите на кнопку "❌ Удалить растение".
    \nЧтобы посмотреть список ваших растений, введите команду /flowers_list.
    \nЧтобы посмотреть статус полива растений, введите команду /watering_status."""
    bot.send_message(message.chat.id, instruction)


@bot.message_handler(commands=['start'])
def start(message):
    sticker = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    # keyboard
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("🌷 Добавить растение")
    item2 = telebot.types.KeyboardButton("❌ Удалить растение")
    item3 = telebot.types.KeyboardButton("🔄 Обновить растение")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

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
    if users_flowers:
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
    else:
        bot.send_message(message.chat.id, "Вы пока что не добавили растений для отслеживания статуса полива!")


@bot.message_handler(commands=['flowers_list'])
def flowers_list(message):
    users_flowers = db.selecting_flowers_from_database(message.chat.id)
    if users_flowers:
        answer = 'Список ваших цветов:'
        mark = 1
        for flower in users_flowers:
            msg = f'\n{mark}) Цветок {flower[1]} типа {flower[2]} с интервалом полива {flower[3]} часов. ' \
                  f'Полит в последний раз {flower[4]}.'
            mark += 1
            answer += msg
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, "Вы еще не добавили ни одного цветка!")


@bot.message_handler(content_types=['text'])
def user_message(message):
    if message.chat.type == 'private':
        if message.text == "🌷 Добавить растение":
            bot.send_message(message.chat.id, "Пожалуйста, введите название растения:")
            bot.register_next_step_handler(message, get_flower_name)
        elif message.text == "❌ Удалить растение":
            bot.send_message(message.chat.id, "Пожалуйста, введите название растения:")
            bot.register_next_step_handler(message, get_flower_name_to_delete)
        elif message.text == "🔄 Обновить растение":
            bot.send_message(message.chat.id, "Пожалуйста, введите название растения:")
            bot.register_next_step_handler(message, get_flower_name_to_update)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢'
                                              '\nДля получения информации о возможностях бота введите команду "/help".')


users_dict = {}


def get_flower_name_to_update(message):
    users_dict[message.chat.id] = [message.text]
    bot.send_message(message.chat.id, "Пожалуйста, введите тип растения:")
    bot.register_next_step_handler(message, get_flower_type_to_update)


def get_flower_type_to_update(message):
    flower_info_list = users_dict[message.chat.id]
    flower_info_list.append(message.text)
    users_dict[message.chat.id] = flower_info_list
    flower = db.select_flower_from_database(message.chat.id, users_dict[message.chat.id][0],
                                            users_dict[message.chat.id][1])
    if flower:
        watering_time = datetime.strptime(flower[4], "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=flower[3])
        current_time = datetime.now()
        if watering_time <= current_time:
            bot.send_message(message.chat.id, "Цветок был полит (да/нет)?")
            bot.register_next_step_handler(message, check_if_flower_was_watered)
        else:
            bot.send_message(message.chat.id, f"Время полива цветка еще не наступило. Цветок нужно будет "
                                              f"полить {watering_time}.")
    else:
        bot.send_message(message.chat.id, 'У вас нет цветка с заданным называнием и типом, но вы можете его добавить '
                                          'с помощью кнопки "🌷 Добавить растение"')


def check_if_flower_was_watered(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, "Цветок был полит во время (да/нет)?")
        bot.register_next_step_handler(message, check_if_flower_was_watered_at_correct_time)
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, "Пожалуйста, полейте цветок!")
    else:
        bot.send_message(message.chat.id, 'Вы ввели информацию некорректно, пожалуйста, напишите "да" или "нет":')
        bot.register_next_step_handler(message, check_if_flower_was_watered)


def check_if_flower_was_watered_at_correct_time(message):
    if message.text.lower() == 'да':
        flower = db.select_flower_from_database(message.chat.id, users_dict[message.chat.id][0],
                                                users_dict[message.chat.id][1])
        watering_time = datetime.strptime(flower[4], "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=flower[3])
        db.update_flower_last_time_watering(message.chat.id, flower[1], flower[2], watering_time)
        bot.send_message(message.chat.id, "Информация о последнем времени полива успешно обновлена!")
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, "Сколько часов назад был полит цветок?")
        bot.register_next_step_handler(message, get_hours_for_last_time_watering)
    else:
        bot.send_message(message.chat.id, 'Вы ввели информацию некорректно, пожалуйста, напишите "да" или "нет":')
        bot.register_next_step_handler(message, check_if_flower_was_watered_at_correct_time)


def get_hours_for_last_time_watering(message):
    try:
        int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели информацию некорректно, пожалуйста, введите цифрами целое число:')
        bot.register_next_step_handler(message, get_hours_for_last_time_watering)
    else:
        flower = db.select_flower_from_database(message.chat.id, users_dict[message.chat.id][0],
                                                users_dict[message.chat.id][1])
        current_time = datetime.now()
        last_time_watered = current_time - timedelta(hours=int(message.text))
        db.update_flower_last_time_watering(message.chat.id, flower[1], flower[2], last_time_watered)
        bot.send_message(message.chat.id, "Информация о последнем времени полива успешно обновлена!")


def get_flower_name_to_delete(message):
    users_dict[message.chat.id] = [message.text]
    bot.send_message(message.chat.id, "Пожалуйста, введите тип растения:")
    bot.register_next_step_handler(message, get_flower_type_to_delete)


def get_flower_type_to_delete(message):
    flower_info_list = users_dict[message.chat.id]
    flower_info_list.append(message.text)
    users_dict[message.chat.id] = flower_info_list
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='yes_delete')
    key_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='no_delete')
    keyboard.add(key_no, key_yes)
    question = f'Проверим инфу для удаления: цветок {users_dict[message.chat.id][0]} ' \
               f'типа {users_dict[message.chat.id][1]}?'
    bot.send_message(message.chat.id, question, reply_markup=keyboard)


def get_flower_name(message):
    users_dict[message.chat.id] = [message.text]
    bot.send_message(message.chat.id, "Пожалуйста, введите тип растения:")
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


# Обработчик ответа на клавиатуре пользователя:
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        current_time = datetime.now()
        db.add_flower_info_to_database(call.message.chat.id, users_dict[call.message.chat.id][0],
                                       users_dict[call.message.chat.id][1], users_dict[call.message.chat.id][2],
                                       current_time)

        # Remove inline buttons and send notification:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Растение сохранено!)", reply_markup=None)
    elif call.data == "no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Начните с начала!)", reply_markup=None)
    elif call.data == "yes_delete":
        flower = db.select_flower_from_database(call.message.chat.id, users_dict[call.message.chat.id][0],
                                                users_dict[call.message.chat.id][1])
        if flower:
            db.delete_flower_from_database(call.message.chat.id, users_dict[call.message.chat.id][0],
                                           users_dict[call.message.chat.id][1])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Растение успешно удалено!)", reply_markup=None)
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Такого цветка нет. Попробуйте снова!", reply_markup=None)
    elif call.data == "no_delete":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Ничего не удалено. Начните с начала!)", reply_markup=None)


bot.polling(none_stop=True)
