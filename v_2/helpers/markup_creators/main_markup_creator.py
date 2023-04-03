from v_2.helpers.markup_creators.add_group_markup_creator import AddGroupMarkupCreator
from v_2.helpers.markup_creators.check_group_markup_creator import CheckGroupMarkupCreator
from v_2.helpers.markup_creators.add_flower_markup_creator import AddFlowerMarkupCreator
from v_2.helpers.markup_creators.check_flower_markup_creator import CheckFlowerMarkupCreator
from v_2.helpers.markup_creators.watering_time_markup_creator import WateringTimeMarkupCreator
from v_2.helpers.markup_creators.back_to_menu_markup_creator import BackToMenuMarkupCreator


class MarkupCreator(AddGroupMarkupCreator, AddFlowerMarkupCreator, CheckFlowerMarkupCreator, CheckGroupMarkupCreator,
                    WateringTimeMarkupCreator, BackToMenuMarkupCreator):
    pass
