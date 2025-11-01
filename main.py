from fastapi import  FastAPI
import config
from database.function_db import start_app
from routers.router import router

app = FastAPI(
    title=config.title_app,
    description=config.description,
    lifespan=start_app
    )


app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=config.port, reload=config.reload)