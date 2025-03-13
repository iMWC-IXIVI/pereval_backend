from dataclasses import dataclass

from fastapi import Form, UploadFile


@dataclass
class ImageBaseFD:
    data: UploadFile = Form(...)
    title: str = Form(...)
