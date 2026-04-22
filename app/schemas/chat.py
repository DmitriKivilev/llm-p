# app/schemas/chat.py

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Схема запроса к LLM."""
    prompt: str = Field(..., description="Основной текст запроса")
    system: str | None = Field(None, description="Необязательная системная инструкция")
    max_history: int = Field(10, ge=1, le=50, description="Сколько сообщений брать из истории")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Креативность модели")


class ChatResponse(BaseModel):
    """Схема ответа от LLM."""
    answer: str

