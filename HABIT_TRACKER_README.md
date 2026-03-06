# Habit Tracker API

A REST API for habit tracking built with Django REST Framework. Tracks daily habit completion, calculates streaks, and provides a 7-day completion history per habit — all per authenticated user.

---

## What It Does

Users can create habits, mark them as complete each day, and track their consistency over time. Each habit automatically calculates:

- Whether it's been completed today
- The current streak (consecutive days completed)
- A 7-day completion history (true/false per day)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 5.2 + Django REST Framework |
| Database | PostgreSQL (SQLite for development) |
| Auth | Django built-in authentication |
| Containerization | Docker + docker-compose |

---

## Project Structure

```
Habit-Tracker/
├── tracker/
│   ├── models.py        # HabitModel, DailyRecordModel
│   ├── serializers.py   # HabitSerializer, DailyRecordSerializer
│   ├── views.py         # HabitView, DailyRecordView (ModelViewSets)
│   └── urls.py          # Router registration
├── habit/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── dockerfile
└── docker-compose.yml
```

---

## API Endpoints

### Habits
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/habits/` | List all habits for authenticated user |
| POST | `/habits/` | Create a new habit |
| GET | `/habits/{id}/` | Get a specific habit |
| PUT | `/habits/{id}/` | Update a habit |
| DELETE | `/habits/{id}/` | Delete a habit |

### Daily Records
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/records/` | List all daily records for authenticated user |
| POST | `/records/` | Mark a habit as complete for today |
| GET | `/records/{id}/` | Get a specific record |
| DELETE | `/records/{id}/` | Delete a record |

---

## Example Response

`GET /habits/1/`

```json
{
  "id": 1,
  "name": "Read 30 minutes",
  "description": "Read before bed every night",
  "created": "2026-02-10T14:53:00Z",
  "is_done_today": true,
  "current_streak": 7,
  "last_7_days": [true, true, false, true, true, true, true]
}
```

---

## Setup

### Option 1 — Docker (Recommended)

```bash
git clone https://github.com/kamalijk007/Task-App-drf--ADHD-
cd Task-App-drf--ADHD-
docker-compose up --build
```

API will be available at `http://localhost:8000/`

### Option 2 — Local

**1. Create and activate a virtual environment**
```bash
python -m venv env
env\Scripts\activate      # Windows
# source env/bin/activate  # Linux/Mac
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

Create a `.env` file in the root:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
```

**4. Run migrations**
```bash
python manage.py migrate
```

**5. Create a superuser**
```bash
python manage.py createsuperuser
```

**6. Start the server**
```bash
python manage.py runserver
```

API will be available at `http://localhost:8000/`

---

## Key Features

**Streak calculation** — Automatically calculates consecutive days a habit has been completed. If today isn't completed yet, the streak counts from yesterday backward.

**7-day history** — Returns a list of 7 booleans representing the last 7 days of completion. Useful for building habit heatmaps or progress bars on the frontend.

**Per-user data isolation** — All habits and records are scoped to the authenticated user. Users can only see and modify their own data.

**Duplicate prevention** — A user cannot log the same habit twice on the same day. Enforced at both the model and serializer level.

---

## Built By

Kamal Khan — Backend & AI Engineer  
[linkedin.com/in/kamal-khan-ai](https://linkedin.com/in/kamal-khan-ai)
