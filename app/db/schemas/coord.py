from pydantic import BaseModel


class CoordBase(BaseModel):
    latitude: float
    longitude: float
    height: int


class CoordCreate(CoordBase):
    pass


class CoordUpdate(CoordBase):
    pass


class CoordRead(CoordBase):
    id: int

    class Config:
        from_attributes = True
