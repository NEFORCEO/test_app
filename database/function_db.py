from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import engine, Base, session_devs


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_session():
    async with session_devs() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session())]


@asynccontextmanager
async def start_app(app: FastAPI):
    print("Приложение запущено")
    await init_db()
    yield
    print("Приложение завершило свою работу")