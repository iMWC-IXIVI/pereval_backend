from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, comment='Идентификатор')
    fam = Column(String, nullable=False, comment='Фамилия')
    name = Column(String, nullable=False, comment='Имя')
    otc = Column(String, nullable=False, comment='Отчество')
    email = Column(String, unique=True, nullable=False, index=True, comment='Почта')
    phone = Column(String, unique=True, nullable=False, comment='Телефон')

    perevals = relationship('Pereval', back_populates='user', cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        return f'User(id={self.id}, email={self.email})'
