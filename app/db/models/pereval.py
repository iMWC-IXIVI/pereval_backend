from enum import Enum as PyEnum

from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class StatusPereval(PyEnum):
    NEW = 'new'
    PEN = 'pending'
    ACC = 'accepted'
    REJ = 'rejected'


class Pereval(Base):
    __tablename__ = 'perevals'

    id = Column(Integer, primary_key=True, comment='Идентификатор')
    beauty_title = Column(String, nullable=False, comment='Короткое название')
    title = Column(String, nullable=False, comment='Название')
    other_title = Column(String, nullable=False, comment='Альтернативное название')
    connect = Column(String, nullable=True, comment='Что соединяет перевал')
    add_time = Column(DateTime, nullable=False, comment='Время отправки')
    status = Column(Enum(StatusPereval), default=StatusPereval.NEW, comment='Статус модерации')

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='Идентификатор пользователя')
    user = relationship('User', back_populates='perevals')

    coord_id = Column(Integer, ForeignKey('coords.id', ondelete='CASCADE'), nullable=False, comment='Идентификатор координат')
    coord = relationship('Coord', back_populates='pereval')

    level_id = Column(Integer, ForeignKey('levels.id', ondelete='CASCADE'), nullable=False, comment='Идентификатор уровней')
    level = relationship('Level', back_populates='pereval')

    def __repr__(self):
        return f'Pereval(id={self.id}, title={self.title})'
