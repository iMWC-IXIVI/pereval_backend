from dataclasses import dataclass
from typing import Optional

from fastapi import Form

from db.models import LevelPereval


@dataclass
class LevelBaseFD:
    winter: LevelPereval = Form(...)
    summer: LevelPereval = Form(...)
    autumn: LevelPereval = Form(...)
    spring: LevelPereval = Form(...)
