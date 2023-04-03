from v_2.helpers.message_handlers.add_flower_message_handler import AddFlowerMessageHandler
from v_2.helpers.message_handlers.add_group_massage_handler import AddGroupMessageHandler
from v_2.helpers.message_handlers.check_group_message_handler import CheckGroupMessageHandler
from v_2.helpers.message_handlers.check_flower_message_handler import CheckFlowerMessageHandler
from v_2.helpers.message_handlers.watering_time_message_handler import WateringTimeMessageHandler
from v_2.helpers.message_handlers.back_to_menu_message_handler import BackToMenuMessageHandler


class MessageHandler(AddGroupMessageHandler, AddFlowerMessageHandler, CheckFlowerMessageHandler,
                     CheckGroupMessageHandler, WateringTimeMessageHandler, BackToMenuMessageHandler):
    pass
