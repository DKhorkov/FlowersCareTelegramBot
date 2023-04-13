import os
import requests
import pickle

from PIL import Image
from telebot.types import File

from .configs import TOKEN
from .photo_paths_handler import PhotoPathsHandler


class PhotoProcessor:

    def save_photo_and_convert_it_to_bytes(self, photo: File, user_id: int) -> bytes:
        photo_path = photo.file_path
        photo_obj = Image.open(requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{photo_path}', stream=True).raw)
        bytes_photo = pickle.dumps(photo_obj)

        self.__check_if_folder_for_photos_exists(user_id=user_id)

        photo_obj.save(f'docker_src/users_photos/{user_id}/flower_photo.png')
        return bytes_photo

    @classmethod
    def __check_if_folder_for_photos_exists(cls, user_id):
        if not os.path.exists(f'docker_src/users_photos'):
            os.mkdir(f'docker_src/users_photos')
        if not os.path.exists(f'docker_src/users_photos/{user_id}'):
            os.mkdir(f'docker_src/users_photos/{user_id}')

    def get_photo_object(self, adding_photo: bool, user_id: int) -> bytes:
        path_to_photo = self.__get_path_to_photo(adding_photo=adding_photo, user_id=user_id)
        with open(os.path.join(os.getcwd(), path_to_photo), 'rb') as file:
            photo = file.read()

        return photo

    @staticmethod
    def __get_path_to_photo(adding_photo: bool, user_id: int) -> str:
        if adding_photo:
            path_to_photo = f'docker_src/users_photos/{user_id}/flower_photo.png'
        else:
            path_to_photo = PhotoPathsHandler.base_flower_picture.value

        return path_to_photo
