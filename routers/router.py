from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select

import config
from database.function_db import SessionDep
from database.model import Devs
from schemas.schema import Dev, Add_devs, Error

router = APIRouter(
    prefix=config.prefix,
    tags=config.tags
)

@router.get(
    "/get_devs",
    response_model=list[Dev]
)
async def get_devs(db: SessionDep):
    get_devs = await db.execute(select(Devs))
    return get_devs.scalars().all()

@router.get(
    '/get_devs/{id}',
    response_model=Dev,
    responses={
        404: {
            "description": "Devs is not Found",
            "model": Error
        }
    }
)
async def get_devs_id(id: int, db: SessionDep):
    result = await db.execute(select(Devs).filter(Devs.dev_id == id))
    id_devs = result.scalars().first()
    
    if not id_devs:
        return JSONResponse(
            status_code=404,
            content={"message": "Такого пользователь не  существует"}
        )
    return Dev(
        dev_id=id_devs.dev_id,
        name=id_devs.name
    )

@router.post(
    "/add_devs",
    response_model=Dev,
    responses={
        409: {
            "description": "Devs is Database",
            "model": Error
        }
    }
)
async def post_devs(devs: Add_devs, db: SessionDep):
    if_devs = await db.execute(select(Devs).filter(Devs.name == devs.name))
    valid_devs = if_devs.scalars().first()
    
    if valid_devs:
        return JSONResponse(
            status_code=409,
            content={"message": "Такой пользователь уже существует"}
        )
    new_devs = Devs(name=devs.name)
    db.add(new_devs)
    await db.commit()
    await db.refresh(new_devs)
    return Dev(
        dev_id=new_devs.dev_id,
        name=new_devs.name
    )    
    
@router.put(
    "/patch_devs/{id}",
    response_model=Dev,
    responses={
        404: {
            "description": "Not found devs",
            "model": Error
            },
    }
)
async def patch_devs(id: int, update:Add_devs,  db: SessionDep):
    devs_patch = await db.execute(select(Devs).filter(Devs.dev_id == id))
    result = devs_patch.scalars().first()
    
    if not result:
        return JSONResponse(
            status_code=404,
            content={"message": "Такого пользователя не существует"}
        )
        
    if update.name is not None:
        result.name = update.name
        
    await db.commit()
    await db.refresh(result)
    return Dev(
        dev_id=result.dev_id,
        name = result.name
    )
    


@router.delete(
    "/delete_devs/{id}",
    response_model=Dev,
    responses={
        404: {
            "description": "Devs not found"
        }
    }
)
async def delete_devs(id: int, db: SessionDep):
    result = await db.execute(select(Devs).filter(Devs.dev_id == id))
    delete_user = result.scalars().first()
    
    if not delete_user:
        return JSONResponse(
            status_code=404,
            content={"message": "Такого пользователь не существует"}
        )
        
    await db.delete(delete_user)
    await db.commit()
    
    return Dev(
        dev_id=delete_user.dev_id,
        name = delete_user.name
    )
    
