# app/core/templates.py
from fastapi.templating import Jinja2Templates
from app.core.utils import adjust_brightness

templates = Jinja2Templates(directory="app/templates")
templates.env.filters["adjust_brightness"] = adjust_brightness
