# src/routers/dashboard.py
from fastapi import APIRouter, Request, Response, Depends, Form
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from typing import Dict, Any

# Импорт наших сервисов и зависимостей
from App.Utility.session_manager import get_session_data, set_session_data
from App.Services.FortyTwoApiService import FortyTwoApiService
from App.Services.GameService import GameService

# Инициализация Jinja2 (должна быть в main.py, но для примера тут)
templates = Jinja2Templates(directory="src/Views")

router = APIRouter()

# Зависимость для проверки аутентификации (аналог "Ensure authentication" в PHP)
async def require_auth(session: Dict[str, Any] = Depends(get_session_data)):
    """Проверяет access_token в сессии. Если нет, редиректит на логин."""
    if not session or not session.get('access_token'):
        # Редирект на главную страницу (где должен быть роут на логин)
        return RedirectResponse(url="/", status_code=302)
    return session

# --- Роут: /dashboard (GET) ---
@router.get("/dashboard")
async def dashboard_view(
    request: Request,
    response: Response,
    auth_result = Depends(require_auth)
):
    """Отображает главную панель: загружает данные 42 API, инициализирует игру и рендерит шаблон."""

    # Если require_auth вернул RedirectResponse, возвращаем его
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    session = auth_result
    api_service = FortyTwoApiService(session=session)
    game_service = GameService(session=session, response=response)

    # 1. Получение данных 42 API (с кэшированием в сессии)
    user_data = await api_service.get_user_data()

    if not user_data:
        # Если не удалось получить данные (например, просрочен токен)
        return RedirectResponse(url="/Auth/logout", status_code=302)

    user_details = api_service.parse_user_details(user_data)
    coalition_data = await api_service.get_coalition_data(user_data.get('id'))

    # 2. Инициализация и получение состояния игры
    game_state = game_service.get_current_state()

    # 3. Сохранение обновленной сессии (с кэшированными user_info и coalition_info)
    await set_session_data(response, session)

    # 4. Рендеринг шаблона
    context = {
        "request": request,
        "first_login_date": session.get('first_login_date'),
        "user": user_details,
        "coalition": coalition_data,
        "state": game_state,
    }
    # Предполагаем, что у вас есть шаблон views/dashboard.html
    return templates.TemplateResponse("dashboard.html", context)


# --- Роут: /dashboard (POST) ---
@router.post("/dashboard")
async def dashboard_post(
    response: Response,
    auth_result = Depends(require_auth),
    # Ожидаем, что клиент отправит action через поле формы
    # Например: <button type="submit" name="action" value="simulate_day">
    action: str = Form(..., description="Action to perform (e.g., 'simulate_day', 'feed', 'work')")
):
    """Обрабатывает игровые действия POST и редиректит обратно на GET-роут."""

    # Если require_auth вернул RedirectResponse, возвращаем его
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    session = auth_result
    game_service = GameService(session=session, response=response)

    # 1. Refresh 42 Data (отдельная логика из PHP-файла)
    if action == 'refresh_data':
        if 'user_info' in session:
            del session['user_info']
        if 'coalition_info' in session:
            del session['coalition_info']

        # Сохраняем сессию после очистки
        await set_session_data(response, session)

        # Редирект для повторного запуска GET-роута
        return RedirectResponse(url="/dashboard", status_code=302)

    # 2. Обработка всех остальных игровых действий
    await game_service.handle_action(action)

    # Принудительный редирект POST->GET для предотвращения повторной отправки формы
    return RedirectResponse(url="/dashboard", status_code=302)
