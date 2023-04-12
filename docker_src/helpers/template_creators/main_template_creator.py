from .add_flower_template_creator import AddFlowerTemplateCreator
from .add_group_template_creator import AddGroupTemplateCreator
from .check_flower_template_creator import CheckFlowerTemplateCreator
from .check_group_template_creator import CheckGroupTemplateCreator
from .watering_time_template_creator import WateringTimeTemplateCreator


class TemplateCreator(AddGroupTemplateCreator, AddFlowerTemplateCreator, CheckFlowerTemplateCreator,
                      CheckGroupTemplateCreator, WateringTimeTemplateCreator):
    pass
