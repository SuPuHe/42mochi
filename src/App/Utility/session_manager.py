import redis.asyncio as redis
from fastapi import Request, Response
from typing import Dict, Any, Optional
import json
import uuid

# Подключение к Redis (имя сервиса из docker-compose)
redis_client = redis.Redis(host='redis', port=6379, db=0)

SESSION_COOKIE_NAME = "session_id"
SESSION_EXPIRY_SECONDS = 7200  # 2 часа


async def get_session_data(request: Request) -> Dict[str, Any]:
    """Получает данные сессии из Redis по session_id из куки."""
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_id:
        return {}

    session_json = await redis_client.get(session_id)
    if session_json:
        await redis_client.expire(session_id, SESSION_EXPIRY_SECONDS)
        try:
            return json.loads(session_json)
        except json.JSONDecodeError:
            return {}

    return {}


async def set_session_data(response: Response, request: Optional[Request], data: Dict[str, Any]):
    """
    Сохраняет данные сессии в Redis.
    Если сессии ещё нет — создаёт новую.
    """
    session_id = request.cookies.get(SESSION_COOKIE_NAME) if request else None

    # Создаем новый session_id, только если нет существующего
    if not session_id:
        session_id = str(uuid.uuid4())
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session_id,
            httponly=True,
            secure=False,  # Если через HTTPS — поменяешь на True
            samesite="lax",
            max_age=SESSION_EXPIRY_SECONDS,
            expires=SESSION_EXPIRY_SECONDS,
        )

    # Сохранить в Redis
    await redis_client.setex(
        session_id,
        SESSION_EXPIRY_SECONDS,
        json.dumps(data)
    )


async def clear_session_data(response: Response, request: Request):
    """Полностью очищает сессию."""
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if session_id:
        await redis_client.delete(session_id)

    response.delete_cookie(SESSION_COOKIE_NAME)
