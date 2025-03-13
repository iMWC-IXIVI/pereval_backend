from dataclasses import dataclass

from fastapi import Form


@dataclass
class CoordBaseFD:
    latitude: float = Form(...)
    longitude: float = Form(...)
    height: int = Form(...)
