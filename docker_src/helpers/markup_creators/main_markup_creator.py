from .add_group_markup_creator import AddGroupMarkupCreator
from .check_group_markup_creator import CheckGroupMarkupCreator
from .add_flower_markup_creator import AddFlowerMarkupCreator
from .check_flower_markup_creator import CheckFlowerMarkupCreator
from .watering_time_markup_creator import WateringTimeMarkupCreator
from .back_to_menu_markup_creator import BackToMenuMarkupCreator


class MarkupCreator(AddGroupMarkupCreator, AddFlowerMarkupCreator, CheckFlowerMarkupCreator, CheckGroupMarkupCreator,
                    WateringTimeMarkupCreator, BackToMenuMarkupCreator):
    pass
