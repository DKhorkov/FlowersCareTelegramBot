from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base


# define declarative Base:
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer(), nullable=False)
    username = Column(Text(), nullable=False)
    first_name = Column(Text(), nullable=False)
    last_name = Column(Text(), nullable=False)
    is_bot = Column(Boolean(), nullable=False)


class FlowersGroup(Base):
    __tablename__ = 'flowers_group'
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer(), ForeignKey('user.user_id'), nullable=False)
    title = Column(Text(), nullable=False)
    description = Column(Text(), nullable=False)
    last_time_watering_date = Column(Text(), nullable=False)
    watering_interval = Column(Text(), nullable=False)
    next_watering_date = Column(Text(), nullable=False)
