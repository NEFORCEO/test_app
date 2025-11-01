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

@router.get("/get_devs", response_model=list[Dev])
async def get_devs(db: SessionDep):
    get_devs = await db.execute(select(Devs))
    return get_devs.scalars().all()

@router.get('/get_devs/{id}', response_model=Dev)
async def get_devs_id(id: int, db: SessionDep):
    result = await db.execute(select(Devs).filter(Devs.dev_id == id))
    id_devs = result.scalars().first()
    
    if not id_devs:
        return Response(
            status_code=404,
            content="Такого пользователя не существует"
        )
    return Dev(
        dev_id=id_devs.dev_id,
        name=id_devs.name
    )

@router.post("/add_devs", response_model=Dev)
async def post_devs(devs: Add_devs, db: SessionDep):
    if_devs = await db.execute(select(Devs).filter(Devs.name == devs.name))
    valid_devs = if_devs.scalars().first()
    
    if valid_devs:
        return Response(
            status_code=409,
            content="Такой пользователь уже существует"
        )
    new_devs = Devs(name=devs.name)
    db.add(new_devs)
    await db.commit()
    await db.refresh(new_devs)
    return Dev(
        dev_id=devs.dev_id,
        name=devs.name
    )    
    
@router.delete("/delete_devs/{id}", response_model=Dev)
async def delete_devs(id: int, db: SessionDep):
    result = await db.execute(select(Devs).filter(Devs.dev_id == id))
    delete_user = result.scalars().first()
    
    if not delete_user:
        return Response(
            status_code=404,
            content="Такого пользователя не существует"
        )
        
    await db.delete(delete_user)
    await db.commit()
    
    return Dev(
        dev_id=delete_user.dev_id,
        name = delete_user.name
    )
    
