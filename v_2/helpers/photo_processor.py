import requests
import pickle

from PIL import Image
from telebot.types import File

from v_2.configs import TOKEN


class PhotoProcessor:

    @staticmethod
    def get_photo_from_message(photo: File) -> bytes:
        photo_path = photo.file_path
        photo_obj = Image.open(requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{photo_path}', stream=True).raw)
        bytes_photo = pickle.dumps(photo_obj)
        return bytes_photo
