from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import JSONResponse
from typing import Dict, Any

from App.Utility.session_manager import get_session_data
from App.Services.GameService import GameService
from routers.dashboard import require_auth

router = APIRouter(prefix="/api")

@router.get("/getMochiStats")
async def get_mochi_stats(
    request: Request,
    response: Response,
    session: Dict[str, Any] = Depends(require_auth)
):
    """Возвращает текущее состояние игры Моти в формате JSON."""
    game_service = GameService(session=session, response=response)
    game_state = game_service.get_current_state()

    return JSONResponse(content=game_state)
