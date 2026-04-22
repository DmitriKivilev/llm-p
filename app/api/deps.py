from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncSession:
    """Предоставить сессию базы данных."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Предоставить репозиторий пользователей."""
    return UserRepository(db)


async def get_chat_repo(db: AsyncSession = Depends(get_db)) -> ChatMessageRepository:
    """Предоставить репозиторий сообщений."""
    return ChatMessageRepository(db)


async def get_llm_client() -> OpenRouterClient:
    """Предоставить клиент OpenRouter."""
    return OpenRouterClient()


async def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    """Предоставить usecase аутентификации."""
    return AuthUseCase(user_repo)


async def get_chat_usecase(
    chat_repo: ChatMessageRepository = Depends(get_chat_repo),
    llm_client: OpenRouterClient = Depends(get_llm_client),
) -> ChatUseCase:
    """Предоставить usecase чата."""
    return ChatUseCase(chat_repo, llm_client)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Получить id текущего пользователя из токена."""
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return int(user_id)
