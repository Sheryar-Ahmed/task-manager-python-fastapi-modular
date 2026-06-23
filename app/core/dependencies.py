from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.modules.auth.utils import decode_token
from app.modules.auth.models import User
from app.core.exceptions import raise_unauthorized_exception

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials
    payload = decode_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise_unauthorized_exception("Invalid token payload")

    user = await User.get(user_id)

    if not user:
        raise_unauthorized_exception("User not found")

    return user