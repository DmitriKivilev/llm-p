# app/schemas/auth.py

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Схема для регистрации пользователя."""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)


class TokenResponse(BaseModel):
    """Схема ответа с JWT токеном."""
    access_token: str
    token_type: str = "bearer"

