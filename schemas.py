from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Literal


# ── Settings ─────────────────────────────────────────────────────────────────

class Settings(BaseModel):
    id:                int
    work_minutes:      int
    short_minutes:     int
    long_minutes:      int
    sessions_per_long: int
    auto_start:        bool
    sound_enabled:     bool
    theme:             str
    updated_at:        Optional[datetime]

    class Config:
        from_attributes = True


class SettingsUpdate(BaseModel):
    work_minutes:      Optional[int]   = Field(None, ge=1, le=60)
    short_minutes:     Optional[int]   = Field(None, ge=1, le=30)
    long_minutes:      Optional[int]   = Field(None, ge=1, le=60)
    sessions_per_long: Optional[int]   = Field(None, ge=1, le=8)
    auto_start:        Optional[bool]  = None
    sound_enabled:     Optional[bool]  = None
    theme:             Optional[Literal["dark", "light"]] = None


# ── Sessions ──────────────────────────────────────────────────────────────────

class SessionCreate(BaseModel):
    mode:         Literal["work", "short", "long"]
    duration_min: int = Field(..., ge=1, le=120)
    completed:    bool = True
    note:         Optional[str] = Field(None, max_length=200)


class Session(BaseModel):
    id:           int
    mode:         str
    duration_min: int
    completed:    bool
    note:         Optional[str]
    created_at:   datetime

    class Config:
        from_attributes = True


# ── Stats ─────────────────────────────────────────────────────────────────────

class Stats(BaseModel):
    total_sessions:    int
    completed_sessions: int
    total_focus_min:   int
    current_streak:    int   # consecutive completed work sessions
    today_sessions:    int
    today_focus_min:   int
