from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.templates import templates  # исправлено, чтобы избежать circular import

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    # редирект на dashboard
    return RedirectResponse("/game")


@router.get("/game", response_class=HTMLResponse)
def game_page(request: Request):
    # временные данные для теста
    displayname = "Guest"
    coalition = "None"
    coalition_color = "#6abc3a"
    sprite_type = "green"

    return templates.TemplateResponse(
        "game.html",
        {
            "request": request,
            "displayname": displayname,
            "coalition": coalition,
            "coalition_color": coalition_color,
            "sprite_type": sprite_type
        }
    )
