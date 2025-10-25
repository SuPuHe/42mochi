# src/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse # <-- Должен быть импортирован

# Импортируем роутеры для каждого контроллера
from routers import home, auth, dashboard, api # и т.д.

templates = Jinja2Templates(directory="src/App/Views")

# Инициализация приложения
app = FastAPI(
    title="Mochi App Backend",
    description="Backend service using FastAPI.",
    version="1.0.0"
)

# 1. Подключение роутеров
app.include_router(home.router, tags=["Home"]) # Обрабатывает корневой путь /
app.include_router(auth.router, prefix="/Auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/Dashboard", tags=["Dashboard"])
app.include_router(api.router, tags=["API"]) # Роут для /api/getMochiStats

# 2. Обработка статических файлов (CSS, JS, Images)
app.mount(
    "/public",
    StaticFiles(directory="public"), # ✅ ИСПРАВЛЕНО: УБРАН ПРЕФИКС 'src/'
    name="public"
)

# 3. Базовый роут (УДАЛЕН: обработка '/' делегирована home.router)
# Функция @app.get("/") удалена, чтобы избежать конфликта.
