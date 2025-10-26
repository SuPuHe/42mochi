from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from typing import Dict, Any

from App.Utility.session_manager import get_session_data, set_session_data
from App.Services.GameService import GameService

templates = Jinja2Templates(directory="src/App/Views")
router = APIRouter()

# --- Зависимость для аутентификации ---
async def require_auth(request: Request) -> dict:
    session = await get_session_data(request)
    if not session or 'user_id' not in session:
        return None
    return session

# --- GET /dashboard ---
@router.get("/dashboard")
async def dashboard_view(request: Request, response: Response, session: dict = Depends(require_auth)):
    if session is None:
        return RedirectResponse(url="/Auth/login", status_code=302)

    game_service = GameService(session=session, response=response, request=request)
    game_state = game_service.get_current_state()

    await set_session_data(response, session)

    context = {
        "request": request,
        "user": session.get("user_info"),
        "state": game_state
    }
    return templates.TemplateResponse("dashboard.html", context)
