from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Level
from db.schemas.form_data import LevelBaseFD


async def level_create(db: AsyncSession, level_data: LevelBaseFD):
    level = Level(
        winter=level_data.winter,
        summer=level_data.summer,
        spring=level_data.spring,
        autumn=level_data.autumn
    )

    db.add(level)

    await db.commit()
    await db.refresh(level)

    return level
