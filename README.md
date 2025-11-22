# Student Grievance Redressal Portal

A complete FastAPI-based web application for managing student grievances with authentication, file uploads, notifications, and admin dashboards.

## ✅ Project Status

**Ready to Run** — All components integrated and tested.

- ✅ Authentication (JWT + bcrypt)
- ✅ Student grievance submission & tracking
- ✅ Admin dashboard & management
- ✅ File uploads with validation
- ✅ Email notifications (BackgroundTasks)
- ✅ Database models (SQLAlchemy + Alembic)
- ✅ Docker & CI/CD (GitHub Actions)
- ✅ Tests (pytest + httpx)

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.11+
- Windows/Linux/Mac with PowerShell or bash

### 1. Clone & Setup

```powershell
cd "f:/student portal/grievance_portal"
python -m venv .venv
& ".venv/Scripts/Activate.ps1"
pip install -r requirements.txt
```

### 2. Set Database (SQLite for dev)

```powershell
$env:DATABASE_URL = "sqlite:///dev.db"
```

### 3. Create Tables (auto on startup)

The app creates tables automatically when started, but you can also:

```powershell
python scripts/create_db.py
```

Or using Alembic:

```powershell
python -m alembic upgrade head
```

### 4. Run

```powershell
python run.py
```

Open: **http://localhost:8000/docs**

## 🧪 Test the API

In Swagger UI (http://localhost:8000/docs):

1. **Register** → POST `/api/v1/auth/register`
   - Email: `student@example.com`
   - Password: `password123`

2. **Login** → POST `/api/v1/auth/login`
   - Copy token from response

3. **Create Grievance** → POST `/api/v1/grievances/`
   - Click 🔒 (Authorize), paste token
   - Submit: `{ "title": "...", "description": "..." }`

4. **List (Admin)** → GET `/api/v1/admin/grievances`

## 📁 Project Structure

```
app/
  ├── main.py                # FastAPI app entry
  ├── api/
  │   ├── v1/
  │   │   ├── auth.py        # Register/login
  │   │   ├── student.py      # Create grievances
  │   │   └── admin.py        # Admin dashboard
  │   └── dependencies.py     # JWT + DB user lookup
  ├── core/
  │   ├── security.py         # Hashing & JWT
  │   ├── config.py           # Settings
  │   └── storage.py          # File upload
  ├── db/
  │   ├── base.py             # SQLAlchemy Base
  │   └── session.py          # Engine & session
  ├── models/
  │   ├── user.py
  │   ├── grievance.py
  │   ├── department.py
  │   ├── audit.py
  │   └── file_upload.py
  └── schemas/
      └── grievance.py        # Pydantic models

migrations/
  └── versions/001_initial.py  # DB schema

tests/
  ├── test_auth.py
  ├── test_grievances.py
  └── ...

Dockerfile, Dockerfile.prod, docker-compose.yml  # Containerization
.github/workflows/ci.yml                         # CI/CD pipeline
```

## 🔧 Configuration

### Environment Variables (see `.env.production.example`)

```bash
# Database
DATABASE_URL=sqlite:///dev.db
# Or for Postgres:
# DATABASE_URL=postgresql://user:pass@localhost:5432/grievance_db

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# SMTP (Email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@grievance.com

# Optional
DEBUG=0
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest -v

# Run specific test file
python -m pytest tests/test_auth.py -v

# With coverage
python -m pytest --cov=app
```

## 🐳 Docker

### Development

```bash
docker build -t grievance-portal:dev .
docker run -p 8000:80 grievance-portal:dev
```

### Production

```bash
docker build -f Dockerfile.prod -t grievance-portal:prod .
docker compose -f docker-compose.yml --env-file .env.production up -d
```

See `README_DEPLOYMENT.md` for full deployment instructions.

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` — Register new user
- `POST /api/v1/auth/login` — Login & get JWT token

### Student
- `POST /api/v1/grievances/` — Create grievance
- `GET /api/v1/grievances/{id}` — Get grievance details

### Admin
- `GET /api/v1/admin/grievances` — List all grievances
- `GET /api/v1/admin/grievances/{id}` — Get grievance (admin view)

### Health
- `GET /` — API health check
- `GET /health` — Health status

## 🔐 Security Features

✅ Password hashing (bcrypt)  
✅ JWT authentication  
✅ Rate limiting (login)  
✅ Admin RBAC (role-based access)  
✅ File upload validation (MIME type, size)  
✅ SQL injection protection (SQLAlchemy ORM)  

## 📧 Notifications

Emails are sent via BackgroundTasks for:
- Grievance created
- Status updated
- Assigned to admin
- Resolved

Configure SMTP in `.env.production.example`.

## 🔄 Database Migrations

### Generate new migration (after model changes)

```bash
python -m alembic revision --autogenerate -m "description"
```

### Apply migrations

```bash
python -m alembic upgrade head
```

### Rollback

```bash
python -m alembic downgrade -1
```

## 📦 Dependencies

See `requirements.txt`:
- FastAPI — Web framework
- SQLAlchemy — ORM
- Alembic — Migrations
- bcrypt — Password hashing
- python-jose — JWT
- pytest — Testing
- python-multipart — File uploads
- And more...

## 🚀 Deployment

### Quick (docker-compose)

```bash
cp .env.production.example .env.production
# Edit .env.production with your values
docker compose up -d
```

### Full Guide

See `README_DEPLOYMENT.md` for:
- Gunicorn + Uvicorn setup
- PostgreSQL/MySQL configuration
- SSL/TLS (Let's Encrypt)
- Systemd services
- Celery background workers

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `no such table` | `python scripts/create_db.py` or `python -m alembic upgrade head` |
| `Address already in use` | Change port: `python -m uvicorn app.main:app --port 8001` |
| bcrypt error on Windows | `pip install bcrypt --only-binary :all:` |
| Can't connect to DB | Check `DATABASE_URL` env var |

## 📖 Documentation

- `QUICKSTART.txt` — 5-minute setup guide
- `README_DEPLOYMENT.md` — Production deployment
- `.env.production.example` — Environment variables
- http://localhost:8000/docs — Interactive API docs (Swagger UI)

## 🤝 Contributing

1. Fork the repo: https://github.com/AtulyaShri/Student-Grievance-Redressal-Portal-Project
2. Create a feature branch: `git checkout -b feature/xyz`
3. Commit changes: `git commit -m "Add feature"`
4. Push: `git push origin feature/xyz`
5. Open a pull request

## 📄 License

MIT License — see LICENSE file for details.

## 📞 Support

Issues? Check:
- GitHub Issues: https://github.com/AtulyaShri/Student-Grievance-Redressal-Portal-Project/issues
- Email: admin@example.com

---

**Built with ❤️ using FastAPI, SQLAlchemy, and Docker**
