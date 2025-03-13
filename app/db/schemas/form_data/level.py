from dataclasses import dataclass
from typing import Optional

from fastapi import Form

from db.models import LevelPereval


@dataclass
class LevelBaseFD:
    winter: Optional[LevelPereval] = Form(None)
    summer: Optional[LevelPereval] = Form(None)
    autumn: Optional[LevelPereval] = Form(None)
    spring: Optional[LevelPereval] = Form(None)
