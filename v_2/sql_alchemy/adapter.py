import logging
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError

from v_2.sql_alchemy.models import Base, User, FlowersGroup, Flower


class SQLAlchemyAdapter:

    def __init__(self, logger: logging.Logger, path_to_db: str ='sqlite_tg_bot_db.db') -> None:
        self._connection = create_engine(
            f"sqlite:///{path_to_db}",
            connect_args={'check_same_thread': False}
        )
        self._Session_base = sessionmaker(bind=self._connection)
        self._session = self._Session_base()
        self._logger = logger

    def create_tables(self) -> None:
        try:
            Base.metadata.create_all(self._connection)
        except InvalidRequestError:
            pass
        except Exception as e:
            self._logger.info(e)

    """
        Ниже идет логика взаимодействия с пользователями.
    """

    def check_if_user_already_registered(self, user_id: int) -> bool | None:
        try:
            user = self._session.query(User).filter(User.user_id == user_id).first()
            if user is None:
                return True
            return False

        except Exception as e:
            self._logger.info(e)

    def add_user(self, user_id: int, username: str, first_name: str, last_name: str, is_bot: bool) ->  None:
        try:
            new_user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_bot=is_bot
            )

            self._session.add(new_user)
            self._session.commit()

            self._logger.info(f'User with id={user_id} and username={username} have subscribed!')

        except Exception as e:
            self._logger.info(e)

    def get_user_id(self, user_id: int) -> int | None:
        try:
            id = self._session.query(User.id).filter(User.user_id == user_id).one()[0]
            return id

        except Exception as e:
            self._logger.info(e)

    """
        Ниже идет логика взаимодействия с группами (сценариями полива).
    """

    def add_flower_group(self, str_user_id: str, json_data: dict) -> None:
        try:
            user_id_from_user_table = self.get_user_id(int(str_user_id))

            new_group = FlowersGroup(
                user_id=user_id_from_user_table,
                title=json_data[str_user_id]['group_title'],
                description=json_data[str_user_id]['group_description'],
                last_time_watering_date=json_data[str_user_id]['last_time_watering_date'],
                watering_interval=json_data[str_user_id]['watering_interval'],
                next_watering_date=json_data[str_user_id]['next_watering_date']
            )

            self._session.add(new_group)
            self._session.commit()

        except Exception as e:
            self._logger.info(e)

    def get_user_flowers_groups(self, user_id: int) -> list[Type[FlowersGroup]] | list:
        try:
            user_id_from_user_table = self.get_user_id(user_id)
            user_flowers_groups = self._session.query(FlowersGroup).filter(
                FlowersGroup.user_id == user_id_from_user_table).all()
            return user_flowers_groups

        except Exception as e:
            self._logger.info(e)

    def get_flowers_group(self, flowers_group_id: int) -> Type[FlowersGroup]:
        try:
            flowers_group = self._session.query(FlowersGroup).filter(FlowersGroup.id == flowers_group_id).one()
            return flowers_group

        except Exception as e:
            self._logger.info(e)

    def delete_flowers_group(self, flowers_group_id: int) -> None:
        try:
            flowers_group_to_delete = self._session.query(FlowersGroup).get(flowers_group_id)
            self._session.delete(flowers_group_to_delete)

            flowers_to_delete = self._session.query(Flower).filter(Flower.group_id == flowers_group_id).all()
            for flower in flowers_to_delete:
                self._session.delete(flower)

            self._session.commit()

        except Exception as e:
            self._logger.info(e)

    """
        Ниже идет логика взаимодействия с цветами (растениями).
    """

    def add_flower(self, str_user_id: str, json_data: dict, bytes_photo: bytes) -> None:
        try:
            user_id_from_user_table = self.get_user_id(int(str_user_id))

            new_flower = Flower(
                user_id=user_id_from_user_table,
                group_id=json_data[str_user_id]['flower_group_id'],
                title=json_data[str_user_id]['flower_title'],
                description=json_data[str_user_id]['flower_description'],
                photo=bytes_photo,
            )

            self._session.add(new_flower)
            self._session.commit()

        except Exception as e:
            self._logger.info(e)

    def get_user_flowers(self, user_id: int) -> list[Type[Flower]] | list:
        try:
            user_id_from_user_table = self.get_user_id(user_id)
            user_flowers = self._session.query(Flower).filter(Flower.user_id == user_id_from_user_table).all()
            return user_flowers

        except Exception as e:
            self._logger.info(e)

    def get_flower(self, flower_id: int) -> Type[Flower]:
        try:
            flower = self._session.query(Flower).filter(Flower.id == flower_id).one()
            return flower

        except Exception as e:
            self._logger.info(e)

    def delete_flower(self, flower_id: int) -> None:
        try:
            flower_to_delete = self._session.query(Flower).get(flower_id)
            self._session.delete(flower_to_delete)
            self._session.commit()

        except Exception as e:
            self._logger.info(e)

    def change_flower_title(self, flower_id: int, new_title: str) -> None:
        try:
            self._session.query(Flower).filter(Flower.id == flower_id).update({Flower.title: new_title})
            self._session.commit()

        except Exception as e:
            self._logger.info(e)

    def change_flower_description(self, flower_id: int, new_description: str) -> None:
        try:
            self._session.query(Flower).filter(Flower.id == flower_id).update({Flower.description: new_description})
            self._session.commit()

        except Exception as e:
            self._logger.info(e)

    def change_flower_photo(self, flower_id: int, new_bytes_photo: bytes) -> None:
        try:
            self._session.query(Flower).filter(Flower.id == flower_id).update({Flower.photo: new_bytes_photo})
            self._session.commit()

        except Exception as e:
            self._logger.info(e)

    def change_flower_group(self, flower_id: int, new_group_id: int) -> None:
        try:
            self._session.query(Flower).filter(Flower.id == flower_id).update({Flower.group_id: new_group_id})
            self._session.commit()

        except Exception as e:
            self._logger.info(e)