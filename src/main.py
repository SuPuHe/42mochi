# src/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# Импортируем роутеры, включая новый api
from routers import home, auth, dashboard, api # <-- Убедитесь, что api здесь!

templates = Jinja2Templates(directory="src/App/Views")

app = FastAPI(
    title="Mochi App Backend",
    description="Backend service using FastAPI.",
    version="1.0.0"
)

# 1. Подключение роутеров
app.include_router(home.router, tags=["Home"])
app.include_router(auth.router, prefix="/Auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/Dashboard", tags=["Dashboard"])
app.include_router(api.router, tags=["API"]) # <-- Включаем роутер API

# 2. Обработка статических файлов (CSS, JS, Images)
# ✅ ИСПРАВЛЕНИЕ: Путь должен быть 'src/public' относительно корня проекта.
app.mount(
    "/public",
    StaticFiles(directory="src/public"),
    name="public"
)

# 3. Базовый роут
@app.get("/", include_in_schema=False)
async def root():
    # Редирект на домашнюю страницу, которую обрабатывает home.router
    return RedirectResponse(url="/", status_code=302)
