from dataclasses import dataclass
from typing import Optional, List, Annotated
from datetime import datetime

from fastapi import Form, Depends, UploadFile

from .user import UserBaseFD
from .coord import CoordBaseFD
from .level import LevelBaseFD


@dataclass
class PerevalBaseFD:
    image_data: Annotated[List[UploadFile], Form()]
    image_title: Annotated[List[str], Form()]

    beauty_title: str = Form(...)
    title: str = Form(...)
    other_title: str = Form(...)
    connect: Optional[str] = Form(None)
    add_time: datetime = Form(...)

    user: UserBaseFD = Depends()
    coord: CoordBaseFD = Depends()
    level: LevelBaseFD = Depends()


class PerevalCreateFD(PerevalBaseFD):
    pass
