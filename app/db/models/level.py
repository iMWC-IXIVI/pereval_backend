from enum import Enum as PyEnum

from sqlalchemy import Column, Enum, Integer
from sqlalchemy.orm import relationship

from .base import Base


class LevelPereval(PyEnum):
    A1 = 'A1'
    A2 = 'A2'
    A3 = 'A3'
    B1 = 'B1'
    B2 = 'B2'
    B3 = 'B3'
    NC = 'NON_CATEGORY'


class Level(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True, comment='Идентификатор')
    winter = Column(Enum(LevelPereval), nullable=False, default=LevelPereval.NC, comment='Зимнее время')
    summer = Column(Enum(LevelPereval), nullable=False, default=LevelPereval.NC, comment='Летнее время')
    spring = Column(Enum(LevelPereval), nullable=False, default=LevelPereval.NC, comment='Весеннее время')
    autumn = Column(Enum(LevelPereval), nullable=False, default=LevelPereval.NC, comment='Осеннее время')

    pereval = relationship('Pereval', back_populates='level', uselist=False, cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        return f'Level(id={self.id})'
