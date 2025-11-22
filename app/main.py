from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, student, admin
from app.db.base import Base
from app.db.session import engine

# Create tables on startup (idempotent)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Grievance Portal API", version="1.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
def root():
    return {"message": "Student Grievance Portal API", "status": "running"}


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(student.router, prefix="/api/v1/grievances", tags=["grievances"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

