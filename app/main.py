from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.database import init_db, disconnect_db
from app.modules.auth.router import router as auth_router
from app.modules.tasks.router import router as tasks_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await disconnect_db()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(tasks_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Something went wrong",
        }
    )

@app.get("/")
async def read_root():
    return {"status": "ok"}