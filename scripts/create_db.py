"""Create database tables from SQLAlchemy models (quick dev helper).
Run: python scripts/create_db.py
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.db.base import Base
from app.db.session import engine

def main():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done")

if __name__ == '__main__':
    main()
