from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.schemas.chat import ChatResponse


class ChatUseCase:
    """логика взаимодействия с LLM."""
    def __init__(self, chat_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self._chat_repo = chat_repo
        self._llm_client = llm_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
    ) -> ChatResponse:
        """отправить запрос к LLM и сохранить историю."""

        await self._chat_repo.add_message(user_id, "user", prompt)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        history = await self._chat_repo.get_last_messages(user_id, limit=max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        answer = await self._llm_client.send_message(messages)

        await self._chat_repo.add_message(user_id, "assistant", answer)

        return ChatResponse(answer=answer)

    async def get_history(self, user_id: int, limit: int = 50):
        """ Получить историю диалога с пользователем"""
        return await self._chat_repo.get_last_messages(user_id, limit)

    async def clear_history(self, user_id: int) -> None:
        """Очистить историю диалога пользователя."""
        await self._chat_repo.delete_all_for_user(user_id)
