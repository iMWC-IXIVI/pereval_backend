import os

from typing import List

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from core.config import settings

from db.schemas.form_data import PerevalBaseFD, PerevalUpdateFD
from db.schemas.json import PerevalRead, ImageRead
from db.crud import image_create, pereval_create, image_pereval_create, user_information
from db.session import get_db
from db.models import Pereval, ImagePereval, Level, Coord

from utils import image_list


router = APIRouter(prefix='/submitData')


@router.post('/', response_model=dict, status_code=201)
async def submit_data_create(db: AsyncSession = Depends(get_db), data: PerevalBaseFD = Depends()):
    try:
        list_image = await image_list(image_data=data.image_data, image_title=data.image_title)

        image = await image_create(db=db, image_data=tuple(list_image))
        pereval = await pereval_create(db=db, pereval_data=data)
        await image_pereval_create(db=db, image_data=tuple(image), pereval_data=pereval)
    except Exception as e:
        return JSONResponse(content={'error': 'can\'t create pereval'}, status_code=400)

    return {'detail': 'success'}


@router.get('/{pk}', response_model=PerevalRead, status_code=200)
async def submit_data_detail(pk: int = Path(..., title='Primary key', ge=1), db: AsyncSession = Depends(get_db)):
    try:
        query = select(Pereval).where(Pereval.id == pk).options(
            selectinload(Pereval.user),
            selectinload(Pereval.coord),
            selectinload(Pereval.level),
            selectinload(Pereval.images_pereval).selectinload(ImagePereval.image)
        )

        result = await db.execute(query)
        pereval = result.scalar_one_or_none()

        images = [ImageRead.model_validate(image.image) for image in pereval.images_pereval]
        pereval_dict = PerevalRead.model_validate(pereval)
        pereval_dict.image = images
    except Exception as e:
        return JSONResponse(content={'error': 'can\'t show detail'}, status_code=400)

    return pereval_dict


@router.get('', response_model=List[PerevalRead], status_code=200)
async def get_user(user_email: str = Query(..., title='User email'), db: AsyncSession = Depends(get_db)):
    try:
        result_list = await user_information(db=db, user_email=user_email)
    except Exception as e:
        return JSONResponse(content={'error': 'can\'t show user information'}, status_code=400)

    return result_list


@router.patch('/{pk}', response_model=dict, status_code=200)
async def submit_data_patch(
        pk: int = Path(..., title='Pereval update (patch)', ge=1),
        db: AsyncSession = Depends(get_db),
        pereval_data: PerevalUpdateFD = Depends()
):
    try:
        query = select(Pereval).where(Pereval.id == pk).options(
            selectinload(Pereval.user),
            selectinload(Pereval.coord),
            selectinload(Pereval.level),
            selectinload(Pereval.images_pereval).selectinload(ImagePereval.image)
        )
        result = await db.execute(query)
        pereval: Pereval = result.scalar_one_or_none()

        coord: Coord = pereval.coord
        level: Level = pereval.level

        pereval.beauty_title = pereval_data.beauty_title
        pereval.title = pereval_data.title
        pereval.other_title = pereval_data.other_title
        pereval.connect = pereval_data.connect

        coord.latitude = pereval_data.coord.latitude
        coord.longitude = pereval_data.coord.longitude
        coord.height = pereval_data.coord.height

        level.winter = pereval_data.level.winter
        level.summer = pereval_data.level.summer
        level.autumn = pereval_data.level.autumn
        level.spring = pereval_data.level.spring

        images = await image_list(image_data=pereval_data.image_data, image_title=pereval_data.image_title)

        for data, instance in zip(images, pereval.images_pereval):
            instance_file_path = os.path.join(settings.MEDIA_DIR, instance.image.data)

            image = data.data
            title = data.title

            image.filename = f'{title}.{image.filename.split(".")[-1]}'
            file_path = os.path.join(settings.MEDIA_DIR, image.filename)

            if os.path.exists(file_path):
                image.filename = f'{settings.generate_unique_value()}{image.filename}'
                file_path = os.path.join(settings.MEDIA_DIR, image.filename)

            with open(file_path, 'wb+') as file:
                file.write(await image.read())

            instance.image.data = image.filename
            instance.image.title = title

            os.remove(instance_file_path)

        await db.commit()
    except Exception as e:
        return JSONResponse(content={'error': 'can\'t update pereval'}, status_code=400)

    return {'message': 'success'}
