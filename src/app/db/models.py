# app/db/models.py
from sqlalchemy import Column, Integer, String, JSON, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    displayname = Column(String)
    coalition = Column(String, default="None")
    coalition_color = Column(String, default="#6abc3a")
    sprite_type = Column(String, default="green")
    game_state = Column(JSON, default={})

# создать таблицы при старте
Base.metadata.create_all(bind=engine)
