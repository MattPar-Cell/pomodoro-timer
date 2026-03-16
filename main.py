from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pomodoro API",
    description="Backend for the Pomodoro timer — sessions, settings, stats.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Settings ────────────────────────────────────────────────────────────────

@app.get("/settings", response_model=schemas.Settings, tags=["Settings"])
def get_settings(db: Session = Depends(get_db)):
    """Return the current settings. Creates defaults if none exist."""
    return crud.get_or_create_settings(db)


@app.put("/settings", response_model=schemas.Settings, tags=["Settings"])
def update_settings(payload: schemas.SettingsUpdate, db: Session = Depends(get_db)):
    """Update one or more settings fields."""
    return crud.update_settings(db, payload)


# ── Sessions ─────────────────────────────────────────────────────────────────

@app.get("/sessions", response_model=list[schemas.Session], tags=["Sessions"])
def list_sessions(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """List completed sessions, newest first."""
    return crud.list_sessions(db, limit=limit, offset=offset)


@app.post("/sessions", response_model=schemas.Session, status_code=201, tags=["Sessions"])
def create_session(payload: schemas.SessionCreate, db: Session = Depends(get_db)):
    """Save a completed pomodoro session."""
    return crud.create_session(db, payload)


@app.delete("/sessions/{session_id}", status_code=204, tags=["Sessions"])
def delete_session(session_id: int, db: Session = Depends(get_db)):
    """Delete a session by ID."""
    if not crud.delete_session(db, session_id):
        raise HTTPException(status_code=404, detail="Session not found")


# ── Stats ─────────────────────────────────────────────────────────────────────

@app.get("/stats", response_model=schemas.Stats, tags=["Stats"])
def get_stats(db: Session = Depends(get_db)):
    """Aggregate stats: total sessions, focus minutes, current streak."""
    return crud.get_stats(db)
