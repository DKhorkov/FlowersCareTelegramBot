from v_2.helpers.message_handlers.add_flower_message_handler import AddFlowerMessageHandler
from v_2.helpers.message_handlers.add_group_massega_handler import AddGroupMessageHandler
from v_2.helpers.message_handlers.check_group_message_handler import CheckGroupMessageHandler
from v_2.helpers.message_handlers.check_flower_message_handler import CheckFlowerMessageHandler


class MessageHandler(AddGroupMessageHandler, AddFlowerMessageHandler, CheckFlowerMessageHandler,
                     CheckGroupMessageHandler):
    pass
