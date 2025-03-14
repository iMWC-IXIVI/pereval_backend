from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from fastapi import HTTPException

from db.schemas.form_data import UserBaseFD
from db.models import User


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


