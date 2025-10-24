from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import home, dashboard, api
import os

app = FastAPI()

# Основная статика
app.mount("/static", StaticFiles(directory=os.path.join("app", "static")), name="static")

# Дополнительные маршруты для js и images
app.mount("/images", StaticFiles(directory=os.path.join("app", "static", "images")), name="images")
app.mount("/js", StaticFiles(directory=os.path.join("app", "static", "js")), name="js")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(home.router)
app.include_router(dashboard.router)
app.include_router(api.router)
