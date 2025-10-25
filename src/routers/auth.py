# src/routers/auth.py
from fastapi import APIRouter, Request, HTTPException, Response, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
import secrets
import httpx
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# Импортируем наши настройки и менеджер сессий
from App.Utility.config import oauth_settings
from App.Utility.session_manager import set_session_data, clear_session_data, get_session_data

# NOTE: Предполагается, что вы добавили set_session_data и clear_session_data
# в App/Utility/session_manager.py. Ниже приведены их заглушки:
# async def set_session_data(response: Response, data: Dict[str, Any]):
#     # Реальная логика: шифрование/подпись куки или запись в Redis
#     response.set_cookie(key="session_id", value="encoded_session_data", httponly=True, secure=True)

# async def clear_session_data(response: Response):
#     # Реальная логика: удаление куки и данных из Redis
#     response.delete_cookie(key="session_id")
#     pass

router = APIRouter()

# --- Роут: /Auth (AuthController::index) ---
@router.get("/")
async def auth_index(request: Request, response: Response):
    """Инициирует процесс OAuth2, редиректя пользователя на 42 API."""

    # 1. Генерация state (аналог bin2hex(random_bytes(8)))
    state = secrets.token_hex(8)

    # NOTE: В FastAPI мы не можем использовать $_SESSION напрямую.
    # Мы должны сохранить state в куках или в кэше, связанном с клиентом.
    # Для простоты сохраним его в куках.
    response.set_cookie(key="oauth_state", value=state, httponly=True, secure=True)

    # (Необязательно) Сохраняем "end_url" для редиректа после логина (аналог $_SESSION['end_url'])
    # В PHP коде он не использовался в index(), но используется в callback().
    # Пусть будет просто редирект на главную страницу (/)

    # 2. Построение URL
    params = {
        'client_id': oauth_settings.client_id,
        'redirect_uri': oauth_settings.redirect_uri,
        'response_type': 'code',
        'scope': 'public',
        'state': state
    }

    # Построение строки запроса и URL
    query_string = httpx.QueryParams(params).url_encoded
    url = f"{oauth_settings.authorize_url}?{query_string}"

    # 3. Редирект
    return RedirectResponse(url=url, status_code=302)

# --- Роут: /Auth/callback (AuthController::callback) ---
@router.get("/callback")
async def auth_callback(request: Request, response: Response):
    """Обрабатывает ответ от 42 API, обменивает код на токен и получает данные пользователя."""

    # 1. Получение параметров и проверка state
    code = request.query_params.get('code')
    state_from_url = request.query_params.get('state')
    state_from_cookie = request.cookies.get('oauth_state')

    # Очищаем cookie state сразу после получения
    response.delete_cookie(key="oauth_state")

    if not code or not state_from_url or state_from_url != state_from_cookie:
        raise HTTPException(status_code=400, detail="Invalid or missing code/state.")

    # 2. Обмен кода на токен (HTTP-POST запрос)
    token_fields = {
        'grant_type': 'authorization_code',
        'client_id': oauth_settings.client_id,
        'client_secret': oauth_settings.client_secret,
        'code': code,
        'redirect_uri': oauth_settings.redirect_uri
    }

    async with httpx.AsyncClient() as client:
        # Запрос токена
        token_response = await client.post(oauth_settings.token_url, data=token_fields)

        if token_response.status_code != 200:
            return HTMLResponse(f"<pre>Failed to get token:\n{token_response.text}</pre>", status_code=500)

        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if not access_token:
             return HTMLResponse(f"<pre>Failed to get access_token:\n{token_response.text}</pre>", status_code=500)

        # 3. Получение данных пользователя (me)
        headers = {"Authorization": f"Bearer {access_token}"}
        user_response = await client.get("https://api.intra.42.fr/v2/me", headers=headers)

        user_info = user_response.json() if user_response.status_code == 200 else None

        if not user_info:
            raise HTTPException(status_code=500, detail="Failed to fetch user info.")

        # 4. Получение данных коалиции
        coalition_info = {'coalition': 'None', 'color': '#6abc3a'}
        user_id = user_info.get('id')

        if user_id:
            coal_url = f"https://api.intra.42.fr/v2/users/{user_id}/coalitions"
            coal_response = await client.get(coal_url, headers=headers)

            coal_data = coal_response.json() if coal_response.status_code == 200 else []

            if isinstance(coal_data, list) and len(coal_data) > 0:
                coalition_info['coalition'] = coal_data[0].get('name', 'None')
                coalition_info['color'] = coal_data[0].get('color', '#6abc3a')

        # 5. Сохранение всего в сессию (вместо $_SESSION)
        session_data = {
            'user_password': 'verified', # Для проверки в HomeController
            'access_token': access_token,
            'refresh_token': token_data.get('refresh_token'),
            'token_expires_at': datetime.now(timezone.utc).timestamp() + token_data.get('expires_in', 7200),
            'user_info': user_info,
            'coalition_info': coalition_info,
            # 'first_login_date': ... (реализовать логику)
        }

        # NOTE: Эта функция должна устанавливать подписанную куку сессии
        await set_session_data(response, session_data)

    # 6. Редирект на главную страницу (аналог $_SESSION['end_url'] или '/')
    # В вашем PHP коде был редирект на $_SESSION['end_url'], по умолчанию будем редиректить на /
    return RedirectResponse(url='/', status_code=302)


# --- Роут: /Auth/logout (AuthController::logout) ---
@router.get("/logout")
async def auth_logout(response: Response, current_session: Optional[Dict[str, Any]] = Depends(get_session_data)):
    """Уничтожает сессию и редиректит на главную."""

    # 1. Уничтожение сессии (куки)
    await clear_session_data(response)

    # 2. Редирект на /
    return RedirectResponse(url='/', status_code=302)
