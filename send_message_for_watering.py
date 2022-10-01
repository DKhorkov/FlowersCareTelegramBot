import time
from datetime import datetime, timedelta
from settings import push_notification_time_to_sleep


def send_messages(database, bot):
    while True:
        flowers = database.select_all_flowers()
        current_time = datetime.now()
        for flower in flowers:
            watering_time = datetime.strptime(flower[4], "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=flower[3])
            if watering_time <= current_time:
                bot.send_message(flower[0], f'Необходимо полить цветок {flower[1]} типа {flower[2]}!')
        time.sleep(push_notification_time_to_sleep)
