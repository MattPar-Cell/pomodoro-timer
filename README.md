# 🍅 Pomodoro — Backend

A lightweight FastAPI backend for the Pomodoro timer. Stores sessions and settings in a local SQLite database — no external services needed.

---

## Stack

- **FastAPI** — API framework
- **SQLAlchemy** — ORM
- **SQLite** — database (file: `pomodoro.db`, auto-created on first run)
- **Pydantic v2** — request/response validation

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn main:app --reload
```

Server starts at **http://localhost:8000**
Interactive API docs at **http://localhost:8000/docs**

---

## API Reference

### Settings

| Method | Endpoint     | Description                        |
|--------|--------------|------------------------------------|
| GET    | `/settings`  | Get current settings               |
| PUT    | `/settings`  | Update one or more settings fields |

**Settings fields:**

| Field              | Type    | Default | Notes                  |
|--------------------|---------|---------|------------------------|
| `work_minutes`     | int     | 25      | 1–60                   |
| `short_minutes`    | int     | 5       | 1–30                   |
| `long_minutes`     | int     | 15      | 1–60                   |
| `sessions_per_long`| int     | 4       | 1–8                    |
| `auto_start`       | bool    | false   |                        |
| `sound_enabled`    | bool    | true    |                        |
| `theme`            | string  | "dark"  | `"dark"` or `"light"`  |

**Example — switch to light mode and set work to 30 min:**
```bash
curl -X PUT http://localhost:8000/settings \
  -H "Content-Type: application/json" \
  -d '{"theme": "light", "work_minutes": 30}'
```

---

### Sessions

| Method | Endpoint              | Description                     |
|--------|-----------------------|---------------------------------|
| GET    | `/sessions`           | List sessions (newest first)    |
| POST   | `/sessions`           | Save a completed session        |
| DELETE | `/sessions/{id}`      | Delete a session                |

**Query params for GET `/sessions`:**
- `limit` (default: 50)
- `offset` (default: 0)

**POST body:**
```json
{
  "mode": "work",
  "duration_min": 25,
  "completed": true,
  "note": "Deep work — project X"
}
```

- `mode`: `"work"` | `"short"` | `"long"`
- `completed`: `false` if the session was interrupted/skipped

---

### Stats

| Method | Endpoint  | Description              |
|--------|-----------|--------------------------|
| GET    | `/stats`  | Aggregated statistics    |

**Response:**
```json
{
  "total_sessions": 12,
  "completed_sessions": 10,
  "total_focus_min": 250,
  "current_streak": 4,
  "today_sessions": 3,
  "today_focus_min": 75
}
```

---

## Project Structure

```
pomodoro-backend/
├── main.py          # FastAPI app, routes
├── database.py      # SQLAlchemy engine & session
├── models.py        # DB table definitions
├── schemas.py       # Pydantic request/response models
├── crud.py          # Database operations
├── requirements.txt
└── README.md
```

---

## Connecting the Frontend

In `pomodoro.html`, the timer can call the API on load/save. Example:

```js
// Load settings on startup
const res = await fetch('http://localhost:8000/settings');
const settings = await res.json();

// Save a completed session
await fetch('http://localhost:8000/sessions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mode: 'work', duration_min: 25, completed: true })
});
```
