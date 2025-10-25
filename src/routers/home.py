from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Dict, Any
from App.Utility.session_manager import get_session_data

# Инициализация шаблонов (должна быть сделана в main.py, но для простоты повторяем)
templates = Jinja2Templates(directory="src/App/Views")

router = APIRouter()

# --- Вспомогательная функция для определения цвета спрайта ---
def get_sprite_type(coalition_color: str) -> str:
    """Определяет тип спрайта (red, purple, green) по HEX-коду."""

    # Удаление # и преобразование в нижний регистр
    hex_code = coalition_color.lstrip('#').lower()
    if len(hex_code) != 6:
        return 'green'

    try:
        # Парсинг RGB
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
    except ValueError:
        return 'green' # Неверный HEX

    # Логика определения доминирующего цвета (как в PHP)
    if r > g and r > b and r > 150:
        return 'red'
    elif b > r and b > g and b > 150:
        return 'purple'
    else:
        return 'green'


def adjust_brightness(hex_code: str, steps: int) -> str:
    """Изменяет яркость HEX-кода цвета."""

    hex_code = hex_code.lstrip('#')
    if len(hex_code) != 6:
        # Возвращаем исходный цвет, если формат неверный
        return hex_code

    try:
        # Конвертация в RGB
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
    except ValueError:
        return hex_code

    # Изменение яркости и ограничение значений (0-255)
    r = max(0, min(255, r + steps))
    g = max(0, min(255, g + steps))
    b = max(0, min(255, b + steps))

    # Конвертация обратно в HEX
    return f'#{r:02x}{g:02x}{b:02x}'


@router.get("/", response_class=HTMLResponse)
async def home_index(request: Request, session: Dict[str, Any] = Depends(get_session_data)):
    # 1. Извлечение данных пользователя и коалиции из сессии
    user_info = session.get('user_info', {})
    coalition_info = session.get('coalition_info', {})

    # 2. Определение, залогинен ли пользователь (по аналогии с PHP)
    logged_in = 'user_password' in session and session.get('user_password') == 'verified'
    displayname = user_info.get('login', 'Guest')
    coalition = coalition_info.get('coalition', 'None')

    # ✅ ИСПРАВЛЕНИЕ ОШИБКИ NameError: Определяем coalition_color, используя дефолтное значение
    coalition_color = coalition_info.get('color', '#6abc3a')

    # 3. Дополнительная логика для спрайта (sprite_type)
    sprite_type = get_sprite_type(coalition_color)

    # 4. ПОДГОТОВКА КОНТЕКСТА И ОТДАЧА ШАБЛОНА

    # НОВАЯ ЛОГИКА: Расчет цветов для CSS
    # Теперь coalition_color определен
    coalition_color_dark = adjust_brightness(coalition_color, -20)
    coalition_color_light = adjust_brightness(coalition_color, 30)

    context = {
        "request": request,
        "displayname": displayname,
        "coalition": coalition,
        "coalition_color": coalition_color,
        "sprite_type": sprite_type,
        # Передаем рассчитанные переменные в шаблон
        "coalition_color_dark": coalition_color_dark,
        "coalition_color_light": coalition_color_light,
    }

    # NOTE: ИСПРАВЛЕНО: Шаблон должен быть game.html, а не game.php
    return templates.TemplateResponse("game.html", context)
