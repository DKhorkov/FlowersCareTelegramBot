from enum import Enum


class PhotoPathsHandler(Enum):

    base_pictures_source = 'helpers/static/images'

    start_picture = f'{base_pictures_source}/start_picture.jpeg'
    base_flower_picture = f'{base_pictures_source}/base_flower_picture.png'
    media_message_picture = f'{base_pictures_source}/media_message_picture.png'
    add_flower_title_picture = f'{base_pictures_source}/add_flower_title_picture.png'
    add_flower_description_picture = f'{base_pictures_source}/add_flower_description_picture.png'
    add_flower_group_picture = f'{base_pictures_source}/add_flower_group_picture.png'
    add_flower_photo_picture = f'{base_pictures_source}/add_flower_photo_picture.png'
    group_title_picture = f'{base_pictures_source}/group_title_picture.png'
    group_description_picture = f'{base_pictures_source}/group_description_picture.png'
    group_last_watering_date_picture = f'{base_pictures_source}/group_last_watering_date_picture.png'
    group_watering_interval_picture = f'{base_pictures_source}/group_watering_interval_picture.png'
    add_group_confirm_data_picture = f'{base_pictures_source}/add_group_confirm_data_picture.png'
    add_group_created_picture = f'{base_pictures_source}/add_group_created_picture.png'