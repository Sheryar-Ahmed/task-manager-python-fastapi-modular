from fastapi import FastAPI
from app.config import settings

app = FastAPI()

@app.get("/")
async def read_root():
    return {"status": "ok", "db": settings.DATABASE_NAME, "jwt_expiration": settings.JWT_EXPIRE_MINUTES}