from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas.form_data import PerevalBaseFD
from db.crud import user_create
from db.session import get_db


router = APIRouter(prefix='/v1')


@router.post('/create/')
async def create(db: AsyncSession = Depends(get_db), data: PerevalBaseFD = Depends()):
    user = await user_create(db=db, user_data=data.user)
    print(user)
    return {'message': 'success'}
