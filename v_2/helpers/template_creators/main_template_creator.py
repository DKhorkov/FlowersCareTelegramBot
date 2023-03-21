from v_2.helpers.template_creators.add_flower_template_creator import AddFlowerTemplateCreator
from v_2.helpers.template_creators.add_group_template_creator import AddGroupTemplateCreator
from v_2.helpers.template_creators.check_flower_template_creator import CheckFlowerTemplateCreator
from v_2.helpers.template_creators.check_group_template_creator import CheckGroupTemplateCreator
from v_2.helpers.template_creators.watering_time_template_creator import WateringTimeTemplateCreator


class TemplateCreator(AddGroupTemplateCreator, AddFlowerTemplateCreator, CheckFlowerTemplateCreator,
                      CheckGroupTemplateCreator, WateringTimeTemplateCreator):
    pass
