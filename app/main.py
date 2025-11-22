from fastapi import FastAPI
from app.api import auth
from app.api import files
from app.api import grievances

app = FastAPI()

app.include_router(auth.router)
app.include_router(files.router)
app.include_router(grievances.router)

