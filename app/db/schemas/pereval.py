from datetime import datetime

from pydantic import BaseModel

from app.db.models import StatusPereval
from .user import UserBase
from .coord import CoordBase
from .level import LevelBase


class PerevalBase(BaseModel):
    beauty_title: str
    title: str
    other_title: str
    connect: str
    add_time: datetime

    user: UserBase
    coord: CoordBase
    level: LevelBase


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
