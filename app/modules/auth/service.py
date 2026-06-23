from app.modules.auth.models import User
from app.modules.auth.schemas import RegisterRequest, LoginRequest
from app.modules.auth.utils import hash_password, verify_password, create_token
from app.core.exceptions import raise_conflict_exception, raise_unauthorized_exception

async def register_user(data: RegisterRequest) -> tuple[User, str]:
    existing = await User.find_one({"email": data.email})
    if existing:
        raise_conflict_exception("Email already registered")

    hashed = hash_password(data.password)
    user = User(name=data.name, email=data.email, password=hashed)
    await user.insert()

    token = create_token(str(user.id))
    return user, token

async def login_user(data: LoginRequest) -> tuple[User, str]:
    user = await User.find_one({"email": data.email})
    if not user or not verify_password(data.password, user.password):
        raise_unauthorized_exception("Invalid email or password")

    token = create_token(str(user.id))
    return user, token