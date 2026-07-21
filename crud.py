"""CRUD operations for the Pomodoro backend.

This module was previously deleted, which broke `main.py`'s import. Restored
here so the FastAPI app runs again. The frontend is local-first and only talks
to this backend when the user flips on "Sync to backend API" in settings.
"""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

import models
import schemas


# ── Settings ──────────────────────────────────────────────────────────────────

def get_or_create_settings(db: Session) -> models.Settings:
    settings = db.query(models.Settings).filter(models.Settings.id == 1).first()
    if settings is None:
        settings = models.Settings(id=1)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


def update_settings(db: Session, payload: schemas.SettingsUpdate) -> models.Settings:
    settings = get_or_create_settings(db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(settings, field, value)
    db.commit()
    db.refresh(settings)
    return settings


# ── Sessions ──────────────────────────────────────────────────────────────────

def list_sessions(db: Session, limit: int = 50, offset: int = 0):
    return (
        db.query(models.Session)
        .order_by(models.Session.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def create_session(db: Session, payload: schemas.SessionCreate) -> models.Session:
    session = models.Session(
        mode=payload.mode,
        duration_min=payload.duration_min,
        completed=payload.completed,
        note=payload.note,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def delete_session(db: Session, session_id: int) -> bool:
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if session is None:
        return False
    db.delete(session)
    db.commit()
    return True


# ── Stats ─────────────────────────────────────────────────────────────────────

def get_stats(db: Session) -> schemas.Stats:
    sessions = db.query(models.Session).all()
    work = [s for s in sessions if s.mode == "work"]
    completed = [s for s in work if s.completed]
    total_focus_min = sum(s.duration_min for s in completed)

    today = datetime.utcnow().date()
    today_work = [s for s in completed if s.created_at and s.created_at.date() == today]

    # current streak: consecutive days (ending today) with >= 1 completed work session
    days_with_focus = {
        s.created_at.date() for s in completed if s.created_at is not None
    }
    streak = 0
    day = today
    while day in days_with_focus:
        streak += 1
        day -= timedelta(days=1)

    return schemas.Stats(
        total_sessions=len(sessions),
        completed_sessions=len(completed),
        total_focus_min=total_focus_min,
        current_streak=streak,
        today_sessions=len(today_work),
        today_focus_min=sum(s.duration_min for s in today_work),
    )
