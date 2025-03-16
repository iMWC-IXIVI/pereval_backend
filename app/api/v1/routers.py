from typing import List

from fastapi import APIRouter, Depends, Path, Query

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select

from db.schemas.form_data import PerevalBaseFD, ImageBaseFD
from db.schemas.json import PerevalRead, ImageRead
from db.crud import image_create, pereval_create, image_pereval_create
from db.session import get_db
from db.models import Pereval, ImagePereval, User


router = APIRouter(prefix='/submitData')


@router.post('/', response_model=dict)
async def submit_data(db: AsyncSession = Depends(get_db), data: PerevalBaseFD = Depends()):
    list_image = []
    for image, title in zip(data.image_data, data.image_title):
        list_image.append(ImageBaseFD(data=image, title=title))

    image = await image_create(db=db, image_data=tuple(list_image))
    pereval = await pereval_create(db=db, pereval_data=data)
    await image_pereval_create(db=db, image_data=tuple(image), pereval_data=pereval)
    return {'message': 'success'}


@router.get('/{pk}', response_model=PerevalRead)
async def submit_data_detail(pk: int = Path(..., title='Primary key', ge=1), db: AsyncSession = Depends(get_db)):
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

    return pereval_dict


@router.get('', response_model=List[PerevalRead])
async def get_user(user_email: str = Query(..., title='User email'), db: AsyncSession = Depends(get_db)):
    query = select(Pereval).join(Pereval.user).where(User.email == user_email).options(
        selectinload(Pereval.coord),
        selectinload(Pereval.level),
        selectinload(Pereval.user),
        selectinload(Pereval.images_pereval).selectinload(ImagePereval.image)
    )
    result = await db.execute(query)
    result = result.scalars().all()

    result_list = []
    for pereval in result:
        images = [ImageRead.model_validate(image.image) for image in pereval.images_pereval]
        pereval_dict = PerevalRead.model_validate(pereval)
        pereval_dict.image = images
        result_list.append(pereval_dict)

    return result_list
