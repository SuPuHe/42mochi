from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
from routers.dashboard import require_auth
from App.Services.GameService import GameService

router = APIRouter()

@router.get("/getMochiStats")
async def get_mochi_stats(request: Request, session: Dict[str, Any] = Depends(require_auth)):
    if session is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    game_service = GameService(session=session, response=None, request=request)
    return JSONResponse(content=game_service.get_current_state())
