from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from beanie import init_beanie

async def init_db():
    from app.modules.auth.models import User
    from app.modules.tasks.models import Task

    client = AsyncIOMotorClient(settings.MONGODB_URL) # gives raw 
    await init_beanie(database=client[settings.DATABASE_NAME], document_models=[User,Task]) # helps us with raw queries easy for us
    
    print(f"Connected To database: {settings.DATABASE_NAME}")

async def disconnect_db():
    print("Disconnected From MongoDB")