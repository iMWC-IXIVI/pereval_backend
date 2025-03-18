from pydantic import BaseModel


class CoordBase(BaseModel):
    latitude: float
    longitude: float
    height: int


class CoordRead(CoordBase):
    id: int

    class Config:
        from_attributes = True
