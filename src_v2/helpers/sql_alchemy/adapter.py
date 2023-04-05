import logging
from datetime import datetime, timedelta
from typing import Type
from telebot.types import Message

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError

from src_v2.helpers.sql_alchemy.models import Base, User, FlowersGroup, Flower, Notification


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
        user = self._session.query(User).filter(User.user_id == user_id).first()
        if user is None:
            return False
        return True

    def add_user(self, message: Message):
        user_id = message.from_user.id,
        username = message.from_user.username,
        first_name = message.from_user.first_name if message.from_user.first_name is not None else 'no name',
        last_name = message.from_user.last_name if message.from_user.last_name is not None else 'no last name',
        is_bot = message.from_user.is_bot

        return self.__add_user(
            user_id=user_id[0],
            username=username[0],
            first_name=first_name[0],
            last_name=last_name[0],
            is_bot=is_bot
        )

    def __add_user(self, user_id: int, username: str, first_name: str, last_name: str, is_bot: bool) ->  None:
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

    def get_user_id(self, message_user_id: int) -> int | None:
        user_id = self._session.query(User.id).filter(User.user_id == message_user_id).one()[0]
        return user_id

    def get_user_by_id(self, user_id: int) -> Type[User]:
        user = self._session.query(User).filter(User.id == user_id).one()
        return user

    """
        Ниже идет логика взаимодействия с группами (сценариями полива).
    """

    def add_group(self, user_id: int, json_data: dict) -> None:
        str_user_id = str(user_id)
        user_id_from_user_table = self.get_user_id(user_id)

        new_group = FlowersGroup(
            user_id=user_id_from_user_table,
            title=json_data[str_user_id]['group_title'],
            description=json_data[str_user_id]['group_description'],
            last_watering_date=json_data[str_user_id]['last_watering_date'],
            watering_interval=json_data[str_user_id]['watering_interval'],
            next_watering_date=json_data[str_user_id]['next_watering_date']
        )

        self._session.add(new_group)
        self._session.commit()

    def get_all_groups(self) -> list[Type[FlowersGroup]] | list:
        flowers_groups = self._session.query(FlowersGroup).all()
        return flowers_groups

    def get_user_groups(self, user_id: int) -> list[Type[FlowersGroup]] | list:
        user_id_from_user_table = self.get_user_id(user_id)
        user_flowers_groups = self._session.query(FlowersGroup).filter(
            FlowersGroup.user_id == user_id_from_user_table).all()
        return user_flowers_groups

    def get_group(self, group_id: int) -> Type[FlowersGroup]:
        flowers_group = self._session.query(FlowersGroup).filter(FlowersGroup.id == group_id).one()
        return flowers_group

    def get_group_flowers(self, group_id: int) -> list[Type[Flower]]:
        group_flowers = self._session.query(Flower).filter(Flower.group_id == group_id).all()
        return group_flowers

    def delete_group(self, group_id: int) -> None:
        """
            Здесь необходимо использовать all, а не one|first, чтобы не словить ошибок, когда еще не было добавлено
            записей в таблицу Notification
        """
        notifications_to_delete = self._session.query(Notification).filter(Notification.group_id == group_id).all()
        for notification in notifications_to_delete:
            self._session.delete(notification)

        flowers_to_delete = self._session.query(Flower).filter(Flower.group_id == group_id).all()
        for flower in flowers_to_delete:
            self._session.delete(flower)

        flowers_group_to_delete = self._session.query(FlowersGroup).get(group_id)
        self._session.delete(flowers_group_to_delete)

        self._session.commit()

    def change_group_title(self, group_id: int, new_title: str) -> None:
        self._session.query(FlowersGroup).filter(FlowersGroup.id == group_id).update({FlowersGroup.title: new_title})
        self._session.commit()

    def change_group_description(self, group_id: int, new_description: str) -> None:
        self._session.query(FlowersGroup).filter(FlowersGroup.id == group_id).update(
            {FlowersGroup.description: new_description}
        )
        self._session.commit()

    def change_group_last_watering_date(self, group_id: int, new_last_watering_date: datetime) -> None:
        group_to_change = self._session.query(FlowersGroup).filter(FlowersGroup.id == group_id).one()
        new_next_watering_date = new_last_watering_date + timedelta(days=group_to_change.watering_interval)

        self._session.query(FlowersGroup).filter(FlowersGroup.id == group_id).update(
            {FlowersGroup.last_watering_date: new_last_watering_date,
             FlowersGroup.next_watering_date: str(new_next_watering_date)
             }
        )
        self._session.commit()

    def change_group_watering_interval(self, group_id: int, new_watering_interval: int) -> None:
        group_to_change = self._session.query(FlowersGroup).filter(FlowersGroup.id == group_id).one()
        new_next_watering_date = datetime.strptime(
            group_to_change.last_watering_date,
            '%Y-%m-%d %H:%M:%S'
        ) + timedelta(days=new_watering_interval)

        self._session.query(FlowersGroup).filter(FlowersGroup.id == group_id).update(
            {FlowersGroup.watering_interval: new_watering_interval,
             FlowersGroup.next_watering_date: str(new_next_watering_date)
             }
        )
        self._session.commit()

    """
        Ниже идет логика взаимодействия с цветами (растениями).
    """

    def add_flower(self, user_id: int, json_data: dict, bytes_photo: bytes) -> None:
        str_user_id = str(user_id)
        user_id_from_user_table = self.get_user_id(user_id)

        new_flower = Flower(
            user_id=user_id_from_user_table,
            group_id=json_data[str_user_id]['flower_group_id'],
            title=json_data[str_user_id]['flower_title'],
            description=json_data[str_user_id]['flower_description'],
            photo=bytes_photo,
        )

        self._session.add(new_flower)
        self._session.commit()

    def get_user_flowers(self, user_id: int) -> list[Type[Flower]] | list:
        user_id_from_user_table = self.get_user_id(user_id)
        user_flowers = self._session.query(Flower).filter(Flower.user_id == user_id_from_user_table).all()
        return user_flowers

    def get_number_of_flowers_in_group(self, group_id: int) -> int:
        number_of_flowers_in_group = self._session.query(Flower).filter(Flower.group_id == group_id).count()
        return number_of_flowers_in_group

    def get_flower(self, flower_id: int) -> Type[Flower]:
        flower = self._session.query(Flower).filter(Flower.id == flower_id).one()
        return flower

    def delete_flower(self, flower_id: int) -> None:
        flower_to_delete = self._session.query(Flower).get(flower_id)
        self._session.delete(flower_to_delete)
        self._session.commit()

    def change_flower_title(self, flower_id: int, new_title: str) -> None:
        self._session.query(Flower).filter(Flower.id == flower_id).update({Flower.title: new_title})
        self._session.commit()

    def change_flower_description(self, flower_id: int, new_description: str) -> None:
        self._session.query(Flower).filter(Flower.id == flower_id).update({Flower.description: new_description})
        self._session.commit()

    def change_flower_photo(self, flower_id: int, new_bytes_photo: bytes) -> None:
        self._session.query(Flower).filter(Flower.id == flower_id).update({Flower.photo: new_bytes_photo})
        self._session.commit()

    def change_flower_group(self, flower_id: int, new_group_id: int) -> None:
        self._session.query(Flower).filter(Flower.id == flower_id).update({Flower.group_id: new_group_id})
        self._session.commit()

    """
        Ниже идет логика взаимодействия с уведомлениями.
    """

    def add_notification(self, group_id: int, message_id: int) -> None:
        new_notification = Notification(
            group_id=group_id,
            message_id=message_id
        )

        self._session.add(new_notification)
        self._session.commit()

    def delete_notification(self, group_id: int) -> None:
        notification_to_delete = self._session.query(Notification).get(group_id)
        self._session.delete(notification_to_delete)
        self._session.commit()

    def change_notification_message_id(self, group_id: int, message_id: int) -> None:
        self._session.query(Notification).filter(Notification.group_id == group_id).update(
            {Notification.message_id: message_id}
        )
        self._session.commit()

    def check_group_notification_existence(self, group_id: int) -> bool:
        notification = self._session.query(Notification).filter(Notification.group_id == group_id).first()
        if notification is None:
            return False
        return True

    def get_notification(self, group_id: int) -> Type[Notification]:
        notification = self._session.query(Notification).filter(Notification.group_id == group_id).one()
        return notification

    def update_last_and_next_watering_dates(self, group_id: int, last_watering_date: str) -> None:
        flowers_group = self._session.query(FlowersGroup).filter(FlowersGroup.id == group_id).one()
        next_watering_date = datetime.strptime(last_watering_date,
            '%Y-%m-%d %H:%M:%S') + timedelta(days=flowers_group.watering_interval)

        self._session.query(FlowersGroup).filter(FlowersGroup.id == group_id).update(
            {FlowersGroup.last_watering_date: last_watering_date,
             FlowersGroup.next_watering_date: str(next_watering_date)}
        )
        self._session.commit()
