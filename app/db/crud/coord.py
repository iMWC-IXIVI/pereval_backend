from sqlalchemy.ext.asyncio import AsyncSession

from db.schemas.form_data import CoordBaseFD
from db.models import Coord


async def coord_create(db: AsyncSession, coord_data: CoordBaseFD):
    coord = Coord(
        latitude=coord_data.latitude,
        longitude=coord_data.longitude,
        height=coord_data.height
    )
    db.add(coord)

    await db.commit()
    await db.refresh(coord)

    return coord
