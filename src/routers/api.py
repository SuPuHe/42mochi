from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any

from App.Utility.session_manager import get_session_data
from App.Services.GameService import GameService
from routers.dashboard import require_auth

router = APIRouter(prefix="/api")

@router.get("/getMochiStats")
async def get_mochi_stats(
    request: Request,
    session: Dict[str, Any] = Depends(require_auth)
):
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    game_service = GameService(session=session, response=None, request=request)
    game_state = game_service.get_current_state()
    return JSONResponse(content=game_state)
