from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class ImagePereval(Base):
    __tablename__ = 'images_pereval'

    id = Column(Integer, primary_key=True, comment='Идентификатор')

    pereval_id = Column(Integer, ForeignKey('perevals.id', ondelete='CASCADE'), nullable=False, comment='Идентификатор перевала')
    pereval = relationship('Pereval', back_populates='images_pereval')

    image_id = Column(Integer, ForeignKey('images.id', ondelete='CASCADE'), nullable=False, comment='Идентификатор изображения')
    image = relationship('Image', back_populates='image_pereval', uselist=False)

    def __repr__(self):
        return f'ImagePereval(id={self.id})'


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, comment='Идентификатор')
    data = Column(String, nullable=False, comment='Изображение')
    title = Column(String, nullable=False, comment='Название')

    image_pereval = relationship('ImagePereval', back_populates='image', uselist=False, cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        return f'Image(id={self.id}, title={self.title}, data={self.data})'
