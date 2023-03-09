from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Text, Boolean, BLOB
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
    flowers_group = relationship("FlowersGroup", passive_deletes=True, cascade='all, delete', back_populates='user')
    flower = relationship("Flower", passive_deletes=True, cascade='all, delete', back_populates='user')


class FlowersGroup(Base):
    __tablename__ = 'flowers_group'
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer(), ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    title = Column(Text(), nullable=False)
    description = Column(Text(), nullable=False)
    last_time_watering_date = Column(Text(), nullable=False)
    watering_interval = Column(Text(), nullable=False)
    next_watering_date = Column(Text(), nullable=False)
    user = relationship("User", passive_deletes=True, cascade='all, delete', back_populates='flowers_group')
    flower = relationship("Flower", passive_deletes=True, cascade='all, delete', back_populates='flowers_group')


class Flower(Base):
    __tablename__ = 'flower'
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer(), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    group_id = Column(Integer(), ForeignKey('flowers_group.id', ondelete='CASCADE'), nullable=False)
    title = Column(Text(), nullable=False)
    description = Column(Text(), nullable=False)
    photo = Column(BLOB(), nullable=False)
    user = relationship("User", passive_deletes=True, cascade='all, delete', back_populates='flower')
    flowers_group = relationship("FlowersGroup", passive_deletes=True, cascade='all, delete', back_populates='flower')
