from sqlalchemy.orm import Session as DBSession
from sqlalchemy import func, desc
from datetime import datetime, date
import models, schemas


# ── Settings ──────────────────────────────────────────────────────────────────

def get_or_create_settings(db: DBSession) -> models.Settings:
    settings = db.query(models.Settings).filter_by(id=1).first()
    if not settings:
        settings = models.Settings(id=1)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


def update_settings(db: DBSession, payload: schemas.SettingsUpdate) -> models.Settings:
    settings = get_or_create_settings(db)
    update_data = payload.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(settings, field, value)
    db.commit()
    db.refresh(settings)
    return settings


# ── Sessions ──────────────────────────────────────────────────────────────────

def list_sessions(db: DBSession, limit: int = 50, offset: int = 0) -> list[models.Session]:
    return (
        db.query(models.Session)
        .order_by(desc(models.Session.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )


def create_session(db: DBSession, payload: schemas.SessionCreate) -> models.Session:
    session = models.Session(**payload.model_dump())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def delete_session(db: DBSession, session_id: int) -> bool:
    session = db.query(models.Session).filter_by(id=session_id).first()
    if not session:
        return False
    db.delete(session)
    db.commit()
    return True


# ── Stats ─────────────────────────────────────────────────────────────────────

def get_stats(db: DBSession) -> schemas.Stats:
    all_sessions = db.query(models.Session).order_by(models.Session.created_at).all()
    today = date.today()

    total_sessions      = len(all_sessions)
    completed_sessions  = sum(1 for s in all_sessions if s.completed)
    total_focus_min     = sum(s.duration_min for s in all_sessions if s.mode == "work" and s.completed)

    today_sessions  = sum(1 for s in all_sessions if s.created_at.date() == today)
    today_focus_min = sum(
        s.duration_min for s in all_sessions
        if s.mode == "work" and s.completed and s.created_at.date() == today
    )

    # Streak: consecutive completed work sessions from most recent backwards
    work_sessions = [s for s in reversed(all_sessions) if s.mode == "work"]
    streak = 0
    for s in work_sessions:
        if s.completed:
            streak += 1
        else:
            break

    return schemas.Stats(
        total_sessions=total_sessions,
        completed_sessions=completed_sessions,
        total_focus_min=total_focus_min,
        current_streak=streak,
        today_sessions=today_sessions,
        today_focus_min=today_focus_min,
    )
