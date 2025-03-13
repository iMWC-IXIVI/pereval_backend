from datetime import datetime

from typing import List

from pydantic import BaseModel

from db.models import StatusPereval
from .user import UserBase
from .coord import CoordBase
from .level import LevelBase
from .image import ImageBase


class PerevalBase(BaseModel):
    beauty_title: str
    title: str
    other_title: str
    connect: str
    add_time: datetime

    user: UserBase
    coord: CoordBase
    level: LevelBase
    image: List[ImageBase]


class PerevalCreate(PerevalBase):
    pass


class PerevalUpdate(PerevalBase):
    pass


class PerevalRead(PerevalBase):
    id: int
    status: StatusPereval

    class Config:
        from_attributes = True
        use_enum_values = True
