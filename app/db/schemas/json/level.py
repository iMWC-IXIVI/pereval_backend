from typing import Optional

from pydantic import BaseModel

from db.models import LevelPereval


class LevelBase(BaseModel):
    winter: Optional[LevelPereval] = None
    summer: Optional[LevelPereval] = None
    spring: Optional[LevelPereval] = None
    autumn: Optional[LevelPereval] = None


class LevelCreate(LevelBase):
    pass


class LevelUpdate(LevelBase):
    pass


class LevelRead(LevelBase):
    id: int

    class Config:
        from_attributes = True
        use_enum_values = True
