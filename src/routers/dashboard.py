from fastapi import APIRouter, Request, Response, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from typing import Dict, Any

from App.Utility.session_manager import get_session_data, set_session_data
from App.Services.FortyTwoApiService import FortyTwoApiService
from App.Services.GameService import GameService

templates = Jinja2Templates(directory="src/Views")
router = APIRouter()

# --- Зависимость для аутентификации ---
async def require_auth(request: Request) -> dict:
    """
    Проверяет аутентификацию пользователя.
    Возвращает словарь сессии, если пользователь авторизован.
    """
    session = await get_session_data(request)  # <- только request

    if not session or 'user_id' not in session:
        if str(request.url.path).startswith("/api"):
            raise HTTPException(status_code=401, detail="Unauthorized")
        return None  # Для веб-страниц будем редиректить в роутах

    return session

# --- GET /dashboard ---
@router.get("/dashboard")
async def dashboard_view(
    request: Request,
    response: Response,
    session: dict = Depends(require_auth)
):
    if session is None:
        return RedirectResponse(url="/Auth/login", status_code=302)

    api_service = FortyTwoApiService(session=session)
    game_service = GameService(session=session, response=response, request=request)

    user_data = await api_service.get_user_data()
    if not user_data:
        return RedirectResponse(url="/Auth/logout", status_code=302)

    user_details = api_service.parse_user_details(user_data)
    coalition_data = await api_service.get_coalition_data(user_data.get('id'))
    game_state = game_service.get_current_state()

    # Сохраняем сессию
    await set_session_data(response, session)

    context = {
        "request": request,
        "first_login_date": session.get('first_login_date'),
        "user": user_details,
        "coalition": coalition_data,
        "state": game_state,
    }
    return templates.TemplateResponse("dashboard.html", context)

# --- POST /dashboard ---
@router.post("/dashboard")
async def dashboard_post(
    request: Request,
    response: Response,
    action: str = Form(...),
    session: dict = Depends(require_auth)
):
    if session is None:
        return RedirectResponse(url="/Auth/login", status_code=302)

    game_service = GameService(session=session, response=response, request=request)

    if action == 'refresh_data':
        session.pop('user_info', None)
        session.pop('coalition_info', None)
        await set_session_data(response, session)
        return RedirectResponse(url="/dashboard", status_code=302)

    await game_service.handle_action(action)
    return RedirectResponse(url="/dashboard", status_code=302)
