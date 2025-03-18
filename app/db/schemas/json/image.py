from pydantic import BaseModel


class ImageBase(BaseModel):
    data: str
    title: str


class ImageRead(ImageBase):
    id: int

    class Config:
        from_attributes = True
