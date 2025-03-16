from datetime import datetime

from typing import List, Optional

from pydantic import BaseModel

from db.models import StatusPereval
from db.schemas.json import UserBase, UserRead, CoordBase, CoordRead, LevelBase, LevelRead, ImageBase, ImageRead


class PerevalBase(BaseModel):
    beauty_title: str
    title: str
    other_title: str
    connect: str
    add_time: datetime

    user: UserBase
    coord: CoordBase
    level: LevelBase
    image: Optional[List[ImageBase]] = None


class PerevalCreate(PerevalBase):
    pass


class PerevalUpdate(PerevalBase):
    pass


class PerevalRead(PerevalBase):
    id: int
    status: StatusPereval

    user: UserRead
    coord: CoordRead
    level: LevelRead
    image: Optional[List[ImageRead]] = None

    class Config:
        from_attributes = True
        use_enum_values = True
