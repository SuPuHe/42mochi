from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api")

@router.get("/getMochiStats")
def get_mochi_stats():
    return JSONResponse({
        "hp": 100,
        "hunger": 50,
        "level": 1
    })
