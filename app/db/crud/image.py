import os

from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Image
from db.schemas.form_data import ImageBaseFD

from core import settings


async def image_create(db: AsyncSession, image_data: Tuple[ImageBaseFD]):
    result_image = []
    for data in image_data:
        image = data.data
        title = data.title

        image.filename = f'{title}.{image.filename.split(".")[-1]}'

        file_path = os.path.join(settings.MEDIA_DIR, image.filename)

        if os.path.exists(file_path):
            image.filename = f'{settings.generate_unique_value()}{image.filename}'
            file_path = os.path.join(settings.MEDIA_DIR, image.filename)

        with open(file_path, 'wb') as file:
            file.write(await image.read())

        image = Image(
            data=image.filename,
            title=title
        )

        db.add(image)

        await db.commit()
        await db.refresh(image)

        result_image.append(image)

    return result_image
