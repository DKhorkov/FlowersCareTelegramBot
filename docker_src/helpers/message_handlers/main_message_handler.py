from .add_flower_message_handler import AddFlowerMessageHandler
from .add_group_massage_handler import AddGroupMessageHandler
from .check_group_message_handler import CheckGroupMessageHandler
from .check_flower_message_handler import CheckFlowerMessageHandler
from .watering_time_message_handler import WateringTimeMessageHandler
from .back_to_menu_message_handler import BackToMenuMessageHandler


class MessageHandler(AddGroupMessageHandler, AddFlowerMessageHandler, CheckFlowerMessageHandler,
                     CheckGroupMessageHandler, WateringTimeMessageHandler, BackToMenuMessageHandler):
    pass
