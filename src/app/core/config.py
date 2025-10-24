# app/core/config.py
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"

JWT_SECRET_KEY = "iOKdTRwpYBf7DYGUxSjHVxiNWZcrZTxW_MRPC0ICHqE"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60
