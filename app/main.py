from fastapi import FastAPI
from app.api.v1 import auth, student, admin

app = FastAPI(title="Student Grievance Portal API")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(student.router, prefix="/api/v1/grievances", tags=["grievances"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
from fastapi import FastAPI
from app.api import auth
from app.api import files
from app.api import grievances

app = FastAPI()

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(grievances.router)

