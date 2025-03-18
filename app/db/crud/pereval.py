from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Pereval
from db.schemas.form_data import PerevalBaseFD

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
