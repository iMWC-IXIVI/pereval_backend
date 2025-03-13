from fastapi import UploadFile

from pydantic import BaseModel


class ImageBase(BaseModel):
    data: UploadFile
    title: str


class ImageCreate(ImageBase):
    pass


class ImageUpdate(ImageBase):
    pass


class ImageRead(ImageBase):
    id: int

    class Config:
        from_attributes = True
