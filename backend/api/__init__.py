from fastapi import FastAPI
from api.routers.faculties.routes import faculties_router
from api.routers.buildings.routes import buildings_router
from api.routers.rooms.routes import rooms_router
from api.routers.programmes.routes import programmes_router
from api.routers.professors.routes import professors_router
from contextlib import asynccontextmanager
from .database.main import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="feedback-unitbv-api", lifespan=lifespan)
app.include_router(faculties_router)
app.include_router(buildings_router)
app.include_router(rooms_router)
app.include_router(programmes_router)
app.include_router(professors_router)
