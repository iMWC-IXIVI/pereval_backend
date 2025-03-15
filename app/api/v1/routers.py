from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas.form_data import PerevalBaseFD, ImageBaseFD
from db.crud import image_create, pereval_create, image_pereval_create
from db.session import get_db


router = APIRouter(prefix='/submitData')


@router.post('/')
async def submit_data(db: AsyncSession = Depends(get_db), data: PerevalBaseFD = Depends()):
    list_image = []
    for image, title in zip(data.image_data, data.image_title):
        list_image.append(ImageBaseFD(data=image, title=title))

    image = await image_create(db=db, image_data=tuple(list_image))
    pereval = await pereval_create(db=db, pereval_data=data)
    await image_pereval_create(db=db, image_data=tuple(image), pereval_data=pereval)
    return {'message': 'success'}
