# app/services/openrouter_client.py

import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    """Клиент для взаимодействия с OpenRouter."""
    
    def __init__(self):
        self._base_url = settings.OPENROUTER_BASE_URL
        self._api_key = settings.OPENROUTER_API_KEY
        self._model = settings.OPENROUTER_MODEL
        self._site_url = settings.OPENROUTER_SITE_URL
        self._app_name = settings.OPENROUTER_APP_NAME

    async def send_message(self, messages: list[dict]) -> str:
        """
        Отправить сообщения в LLM и получить ответ.
        """

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": self._site_url,
            "X-Title": self._app_name,
            "Content-Type": "application/json",
        }

        payload = {
            "model": self._model,
            "messages": messages,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self._base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                print(f"DEBUG: {data}")
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
                else:
                    return "Ошибка: нет ответа от модели"
            except httpx.HTTPStatusError as e:
                raise ExternalServiceError(f"OpenRouter API error: {e.response.status_code}")
            except Exception as e:
                raise ExternalServiceError(f"OpenRouter connection error: {str(e)}")

