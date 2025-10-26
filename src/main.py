from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from routers import home, auth, dashboard, api

app = FastAPI(
    title="Mochi App Backend",
    description="Backend service using FastAPI.",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(home.router, tags=["Home"])
app.include_router(auth.router, prefix="/Auth", tags=["Authentication"])
app.include_router(dashboard.router, tags=["Dashboard"])  # без префикса
app.include_router(api.router, prefix="/api", tags=["API"])

# Статические файлы
app.mount("/public", StaticFiles(directory="src/public"), name="public")

# Редирект с корня на /dashboard
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/dashboard", status_code=302)
