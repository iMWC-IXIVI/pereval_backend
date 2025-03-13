from fastapi import APIRouter, Depends

from db.schemas.form_data import PerevalBaseFD


router = APIRouter(prefix='/v1')


@router.post('/create/')
async def create(data: PerevalBaseFD = Depends()):
    print(data)
    return {'message': 'success'}
