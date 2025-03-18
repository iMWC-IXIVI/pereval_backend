from typing import List

from fastapi import UploadFile

from db.schemas.form_data import ImageBaseFD


async def image_list(image_data: List[UploadFile], image_title: List[str]):
    result_list = []
    for image, title in zip(image_data, image_title):
        result_list.append(ImageBaseFD(data=image, title=title))

    return result_list
