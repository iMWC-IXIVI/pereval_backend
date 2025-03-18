from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Pereval, ImagePereval, Coord, Level
from db.schemas.form_data import PerevalBaseFD, PerevalUpdateFD
from db.schemas.json import PerevalRead, ImageRead

from db.crud import user_create, coord_create, level_create


async def pereval_create(db: AsyncSession, pereval_data: PerevalBaseFD):
    user = await user_create(db=db, user_data=pereval_data.user)
    coord = await coord_create(db=db, coord_data=pereval_data.coord)
    level = await level_create(db=db, level_data=pereval_data.level)

    pereval = Pereval(
        beauty_title=pereval_data.beauty_title,
        title=pereval_data.title,
        other_title=pereval_data.other_title,
        connect=pereval_data.connect,
        add_time=pereval_data.add_time,

        user_id=user.id,
        coord_id=coord.id,
        level_id=level.id
    )

    db.add(pereval)

    await db.commit()
    await db.refresh(pereval)

    return pereval


async def pereval_detail(pk:int, db: AsyncSession):
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


async def pereval_update(db: AsyncSession, pereval_data: PerevalUpdateFD, pk: int):
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

    return pereval
