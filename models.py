from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from database import Base


class Settings(Base):
    __tablename__ = "settings"

    id               = Column(Integer, primary_key=True, default=1)
    work_minutes     = Column(Integer, default=25)
    short_minutes    = Column(Integer, default=5)
    long_minutes     = Column(Integer, default=15)
    sessions_per_long = Column(Integer, default=4)
    auto_start       = Column(Boolean, default=False)
    sound_enabled    = Column(Boolean, default=True)
    theme            = Column(String, default="dark")   # "dark" | "light"
    updated_at       = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Session(Base):
    __tablename__ = "sessions"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    mode         = Column(String, nullable=False)          # "work" | "short" | "long"
    duration_min = Column(Integer, nullable=False)         # actual minutes set
    completed    = Column(Boolean, default=True)           # False = interrupted
    note         = Column(String, nullable=True)           # optional label/tag
    created_at   = Column(DateTime, server_default=func.now())
