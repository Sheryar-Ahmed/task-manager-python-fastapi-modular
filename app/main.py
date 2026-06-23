from fastapi import FastAPI
from app.config import settings
from contextlib import asynccontextmanager
from app.database import init_db, disconnect_db
from app.modules.auth.router import router as auth_router
from app.modules.tasks.router import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await disconnect_db()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(tasks_router)

@app.get("/")
async def read_root():
    return {"status": "ok", "db": settings.DATABASE_NAME, "jwt_expiration": settings.JWT_EXPIRE_MINUTES}