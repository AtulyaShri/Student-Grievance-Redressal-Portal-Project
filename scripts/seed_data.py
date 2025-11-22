"""Seed initial test data into the database.
Run after creating tables:
  python scripts/seed_data.py
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.db.session import SessionLocal
from app.models.user import User
from app.models.department import Department
from app.core.security import get_password_hash


def seed_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Data already seeded. Skipping.")
            return

        # Create admin user
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
            is_active=True
        )
        db.add(admin)

        # Create test student
        student = User(
            email="student@example.com",
            hashed_password=get_password_hash("password123"),
            is_admin=False,
            is_active=True
        )
        db.add(student)

        # Create departments
        departments = [
            Department(name="Academic Affairs"),
            Department(name="Admissions"),
            Department(name="Student Services"),
            Department(name="Finance"),
            Department(name="Infrastructure"),
        ]
        for dept in departments:
            db.add(dept)

        db.commit()
        print("✓ Seeded admin user: admin@example.com / admin123")
        print("✓ Seeded test student: student@example.com / password123")
        print(f"✓ Seeded {len(departments)} departments")
    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
