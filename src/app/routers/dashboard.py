from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.templates import templates  # исправлено, чтобы избежать circular import

router = APIRouter()


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    game_state = {
        "hp": 100,
        "days": 0,
        "coins": 10,
        "food": 0,
        "monster_hp": 100,
        "monster_level": 1,
        "hunger": 100,
        "logs": []
    }
    displayname = "Guest"
    coalition = "None"
    coalition_color = "#6abc3a"
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "displayname": displayname,
            "coalition": coalition,
            "coalition_color": coalition_color,
            "game_state": game_state
        }
    )


@router.post("/dashboard/action")
def dashboard_action(
    request: Request,
    feed: str = Form(None),
    work: str = Form(None)
):
    # Здесь можно подключить DB и обновлять game_state
    # Пока редирект на страницу dashboard
    return RedirectResponse("/dashboard", status_code=303)
