# Nirnaya Vidhi AI – Backend

Django + DRF backend for Nirnaya Vidhi AI.

This backend provides:
- Clerk-based JWT authentication
- RAG (Retrieval-Augmented Generation) endpoints
- LLM integration layer
- Vector search services
- System health/status endpoints
- Modular service architecture

---

## Architecture Overview

Frontend (Next.js + Clerk)
        ↓
Clerk issues JWT
        ↓
Django REST API (Verifies Clerk JWT)
        ↓
RAG Services → LLM Service → Vector Service
        ↓
Database / Vector Store

Authentication is fully handled by Clerk.
Django only verifies Clerk-issued JWT tokens.

---

## Project Structure
```txt
nirnaya-vidhi-ai/
│
├── api/                         # Main Django app (business logic layer)
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── authentication.py        # Clerk JWT authentication class
│   ├── models.py                # Database models
│   ├── serializers.py           # DRF serializers
│   ├── tests.py
│   ├── urls.py                  # App-level URL routing
│   │
│   ├── views/                   # API view layer (thin controllers)
│   │   ├── rag_views.py         # RAG endpoints
│   │   └── system_views.py      # Health & status endpoints
│   │
│   ├── services/                # Business logic layer
│   │   ├── llm_service.py       # LLM interaction logic
│   │   └── vector_service.py    # Vector search & embeddings logic
│   │
│   └── migrations/              # Django migrations
│       └── __init__.py
│
├── core/                        # Django project configuration
│   ├── __init__.py
│   ├── settings.py              # Global settings
│   ├── urls.py                  # Root URL configuration
│   ├── asgi.py                  # ASGI entrypoint
│   └── wsgi.py                  # WSGI entrypoint
│
├── manage.py                    # Django CLI entrypoint
├── requirements.txt             # Python dependencies
├── test_db.py                   # Manual DB test script
├── test_llm.py                  # Manual LLM test script
├── .env                         # Environment variables (not committed)
├── .gitignore
└── venv/                        # Virtual environment (not committed)
```

---

## Authentication Design

1. User logs in via Clerk (frontend).
2. Clerk issues JWT.
3. Frontend sends:

   Authorization: Bearer <clerk_token>

4. Django verifies token using Clerk JWKS.
5. If valid → request proceeds.

Django:
- Does NOT manage passwords
- Does NOT issue JWT
- Does NOT manage sessions

---

## Setup Instructions

### 1. Clone Repository

git clone https://github.com/urwithajit9/nirnaya-vidhiai-backend.git
cd nirnaya-vidhi-ai

### 2. Create Virtual Environment

python -m venv venv
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Create .env File

Create a `.env` file in project root:

DEBUG=True
SECRET_KEY=your-secret-key

CLERK_ISSUER=https://your-domain.clerk.accounts.dev
CLERK_AUDIENCE=your-audience-if-used

DATABASE_URL=sqlite:///db.sqlite3

If not validating audience, remove CLERK_AUDIENCE.

### 5. Run Migrations

python manage.py migrate

### 6. Run Server

python manage.py runserver

Server runs at:

http://127.0.0.1:8000/

---

## Testing Endpoints

### Public Endpoints

GET /api/v1/system/status
GET /api/v1/system/health-check

Example:

curl http://127.0.0.1:8000/api/v1/system/status

### Protected Endpoints

Require Clerk JWT:

curl http://127.0.0.1:8000/api/v1/rag/query \
  -H "Authorization: Bearer YOUR_CLERK_TOKEN"

---

## Services Layer

llm_service.py
- Prompt construction
- LLM calls
- Response formatting

vector_service.py
- Embeddings
- Vector similarity search
- Retrieval logic

Views remain thin.
Business logic lives in services.

---

## Recommended Production Stack

- Gunicorn + Uvicorn workers
- PostgreSQL
- Redis (optional caching)
- Nginx
- Environment-based configuration

---

## Future Improvements

- Role-based permissions
- Multi-tenant org support (Clerk Organizations)
- Redis caching
- Background jobs (Celery/RQ)
- Rate limiting
- Structured logging
