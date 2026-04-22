# app/usecases/auth.py

from app.repositories.users import UserRepository
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.schemas.user import UserPublic
from app.schemas.auth import TokenResponse


class AuthUseCase:
    """B - логика аутентификации и регистрации."""
    
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def register(self, email: str, password: str) -> UserPublic:
        """Регистрация нового пользователя."""
        existing_user = await self._user_repo.get_by_email(email)
        if existing_user:
            raise ConflictError("User with this email already exists")
        
        password_hash = get_password_hash(password)
        user = await self._user_repo.create(email=email, password_hash=password_hash)
        return UserPublic.model_validate(user)

    async def login(self, email: str, password: str) -> TokenResponse:
        """Вход пользователя, выдача токена."""
        user = await self._user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Wrong  email or password")
        
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Wrong  email or password")
        
        token_data = {"sub": str(user.id), "role": user.role}
        access_token = create_access_token(token_data)
        return TokenResponse(access_token=access_token)

    async def get_me(self, user_id: int) -> UserPublic:
        """Получить профиль текущего пользователя."""
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return UserPublic.model_validate(user)
