# src/App/Utility/session_manager.py (С РЕАЛИЗАЦИЕЙ REDIS)
import redis.asyncio as redis
from fastapi import Request, HTTPException, Response
from typing import Dict, Any, Optional
import json
import uuid

# Инициализируем Redis-клиент (имя хоста 'redis' берется из docker-compose)
redis_client = redis.Redis(host='redis', port=6379, db=0)
SESSION_COOKIE_NAME = "session_id"
SESSION_EXPIRY_SECONDS = 7200 # 2 часа

# --- ФУНКЦИИ СЕССИИ ---

async def set_session_data(response: Response, data: Dict[str, Any]):
    """Генерирует ID, сохраняет данные в Redis и устанавливает HTTP-куку."""
    session_id = str(uuid.uuid4())
    # Сохраняем данные как JSON в Redis
    await redis_client.setex(
        session_id,
        SESSION_EXPIRY_SECONDS,
        json.dumps(data)
    )

    # Устанавливаем куку, связанную с ID
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        secure=True,
        max_age=SESSION_EXPIRY_SECONDS,
        expires=SESSION_EXPIRY_SECONDS
    )

async def get_session_data(request: Request) -> Dict[str, Any]:
    """Извлекает данные сессии из Redis по ID куки."""
    session_id = request.cookies.get(SESSION_COOKIE_NAME)

    if not session_id:
        return {}

    session_json = await redis_client.get(session_id)

    if session_json:
        # Продлеваем сессию при активности
        await redis_client.expire(session_id, SESSION_EXPIRY_SECONDS)
        return json.loads(session_json)

    return {}

async def clear_session_data(response: Response):
    """Удаляет данные из Redis и очищает HTTP-куку."""
    session_id = response.request.cookies.get(SESSION_COOKIE_NAME)

    if session_id:
        await redis_client.delete(session_id)

    # Удаляем куку, устанавливая время жизни в прошлое
    response.delete_cookie(key=SESSION_COOKIE_NAME)
