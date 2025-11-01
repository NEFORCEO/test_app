from fastapi import APIRouter, Response
from sqlalchemy import select

import config
from database.function_db import SessionDep
from database.model import Devs
from schemas.schema import Dev, Add_devs

router = APIRouter(
    prefix=config.prefix,
    tags=config.tags
)

@router.get("/get_devs")
async def get_devs(db: SessionDep) -> list[Dev]:
    get_devs = await db.execute(select(Devs))
    return get_devs.scalars().all()

@router.post('/add_devs')
async def post_devs(devs: Add_devs, db: SessionDep) -> Dev:
    if_valid_dev = await db.execute(select(Dev).filter(Dev.name == devs.name))
    valid_dev = if_valid_dev.scalars().first()

    if valid_dev:
        return Response(
            status_code=409,
            content="Пользователь уже существует"
        )
    new_devs = Devs(name=devs.name)
    db.add(new_devs)
    await db.commit()
    await db.refresh(new_devs)