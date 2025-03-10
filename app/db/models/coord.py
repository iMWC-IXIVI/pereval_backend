from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship

from .base import Base


class Coord(Base):
    __tablename__ = 'coords'

    id = Column(Integer, primary_key=True, comment='Идентификатор')
    latitude = Column(Float, nullable=False, comment='Широта')
    longitude = Column(Float, nullable=False, comment='Долгота')
    height = Column(Integer, nullable=False, comment='Высота')

    pereval = relationship('Pereval', back_populates='coord', uselist=False, cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        return f'Coords(id={self.id})'
