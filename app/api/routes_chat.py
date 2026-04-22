from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user_id, get_chat_usecase
from app.usecases.chat import ChatUseCase
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.errors import ExternalServiceError

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Отправить сообщение в LLM и получить ответ."""
    try:
        return await usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history,
        )
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))


@router.get("/history")
async def get_history(
    limit: int = 50,
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
):
    messages = await usecase.get_history(user_id, limit)
    return [
        {
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
        }
        for msg in messages
    ]


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
):
    await usecase.clear_history(user_id)
