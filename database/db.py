import config

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import declarative_base,sessionmaker


engine = create_async_engine(config.db_url)

session_devs = sessionmaker(bind=engine,class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()