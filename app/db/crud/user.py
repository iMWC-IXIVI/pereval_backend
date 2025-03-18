from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from fastapi import HTTPException

from db.schemas.form_data import UserBaseFD
from db.schemas.json import PerevalRead, ImageRead
from db.models import User, Pereval, ImagePereval


async def user_query(db: AsyncSession, user_data: UserBaseFD):
    query = select(User).filter(or_(User.email == user_data.email, User.phone == user_data.phone))
    result = await db.execute(query)

    return result.fetchone()


async def user_create(db: AsyncSession, user_data: UserBaseFD):
    old_user = await user_query(db=db, user_data=user_data)
    if old_user:
        return old_user[0]

    user = User(
        fam=user_data.fam,
        name=user_data.name,
        otc=user_data.otc,
        email=user_data.email,
        phone=user_data.phone
    )

    db.add(user)

    try:
        await db.commit()
        await db.refresh(user)

        return user
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail='A user with such email or phone number has been created')


async def user_information(db: AsyncSession, user_email: str):
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
