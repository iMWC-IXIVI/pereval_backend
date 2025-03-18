from typing import List

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas.form_data import PerevalBaseFD, PerevalUpdateFD
from db.schemas.json import PerevalRead
from db.crud import image_create, pereval_create, image_pereval_create, user_information, pereval_detail, pereval_update, image_update
from db.session import get_db
from db.models import Pereval

from core import logger

from utils import image_list


router = APIRouter(prefix='/submitData')


@router.post('/', response_model=dict, status_code=201)
async def submit_data_create(db: AsyncSession = Depends(get_db), data: PerevalBaseFD = Depends()):
    try:
        logger.debug_message(f'Отправляемые данные - {data}')

        logger.info_message('Формирование списка фотографий!!!')
        list_image = await image_list(image_data=data.image_data, image_title=data.image_title)
        logger.info_message('Функция по созданию списка завершилась успешно!!!')

        logger.info_message('Сохранение фотографии!!!')
        image = await image_create(db=db, image_data=tuple(list_image))
        logger.info_message('Сохранение фотографии завершилась успешно!!!')

        logger.info_message('Сохранение перевала в базе данных!!!')
        pereval = await pereval_create(db=db, pereval_data=data)
        logger.info_message('Сохранение перевела завершилась успешно!!!')

        logger.info_message('Создание записи в ImagesPereval!!!')
        await image_pereval_create(db=db, image_data=tuple(image), pereval_data=pereval)
        logger.info_message('Создание записи в ImagesPereval завершилась успешно!!!')
    except Exception as e:
        logger.error_message(f'По данной причине не удалось создать запись в бд - {e}')
        return JSONResponse(content={'error': 'can\'t create pereval'}, status_code=400)

    return {'detail': 'success'}


@router.get('/{pk}', response_model=PerevalRead, status_code=200)
async def submit_data_detail(pk: int = Path(..., title='Primary key', ge=1), db: AsyncSession = Depends(get_db)):
    try:
        pereval_dict = await pereval_detail(pk=pk, db=db)
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
        pereval: Pereval = await pereval_update(db=db, pereval_data=pereval_data, pk=pk)
        images = await image_list(image_data=pereval_data.image_data, image_title=pereval_data.image_title)
        await image_update(pereval=pereval, images=images)

        await db.commit()
    except Exception as e:
        return JSONResponse(content={'error': 'can\'t update pereval'}, status_code=400)

    return {'message': 'success'}
