from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError

from .models import Base, User, FlowersGroup


class SQLAlchemyAdapter:

    def __init__(self, logger, path_to_db='sqlite_tg_bot_db.db'):
        self._connection = create_engine(
            f"sqlite:///{path_to_db}",
            connect_args={'check_same_thread': False}
        )
        self._Session_base = sessionmaker(bind=self._connection)
        self._session = self._Session_base()
        self._logger = logger

    def create_tables(self):
        try:
            Base.metadata.create_all(self._connection)
        except InvalidRequestError:
            pass
        except Exception as e:
            self._logger.info(e)

    def check_if_user_already_registered(self, user_id):
        try:
            user = self._session.query(User).filter(User.user_id == user_id).first()
            if user is None:
                return True
            return False

        except Exception as e:
            self._logger.info(e)

    def add_user(self, user_id, username, first_name, last_name, is_bot):
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

    def get_user_id(self, user_id):
        try:
            id = self._session.query(User.id).filter(User.user_id == user_id).one()[0]
            return id

        except Exception as e:
            self._logger.info(e)

    def add_flower_group(self, str_user_id, json_data):
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

