import os
import requests
import pickle

from PIL import Image
from telebot.types import File

from v_2.configs import TOKEN


class PhotoProcessor:

    @staticmethod
    def get_photo_from_message(photo: File, user_id: int) -> bytes:
        photo_path = photo.file_path
        photo_obj = Image.open(requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{photo_path}', stream=True).raw)
        bytes_photo = pickle.dumps(photo_obj)

        if not os.path.exists(f'users_photos'):
            os.mkdir(f'users_photos')
        if not os.path.exists(f'users_photos/{user_id}'):
            os.mkdir(f'users_photos/{user_id}')

        photo_obj.save(f'users_photos/{user_id}/flower_photo.png')
        return bytes_photo
