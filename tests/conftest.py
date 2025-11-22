"""
Pytest fixtures and configuration for integration tests.
"""
import pytest
from httpx import AsyncClient
from app.main import app
from app.core.security import create_access_token


@pytest.fixture
async def async_client():
    """Provide an async HTTP client for the app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_user_data():
    """Test user credentials."""
    return {
        "email": "testuser@example.com",
        "password": "TestPassword123!",
    }


@pytest.fixture
def test_user_with_id():
    """Test user data with ID."""
    return {
        "id": 1,
        "email": "testuser@example.com",
        "password": "TestPassword123!",
        "is_active": True,
    }


@pytest.fixture
def test_token(test_user_with_id):
    """Generate a test JWT token."""
    token = create_access_token(
        data={"sub": str(test_user_with_id["id"]), "email": test_user_with_id["email"]}
    )
    return token


@pytest.fixture
def auth_headers(test_token):
    """Headers with Bearer token for authenticated requests."""
    return {"Authorization": f"Bearer {test_token}"}


@pytest.fixture
def test_grievance_data():
    """Test grievance creation data."""
    return {
        "title": "Broken Lab Equipment",
        "category": "Facilities",
        "description": "The microscope in Lab B is not working properly.",
        "dept_id": 1,
    }


@pytest.fixture
def test_file_data():
    """Test file upload data."""
    return {
        "filename": "test_document.pdf",
        "content": b"%PDF-1.4 test content",
        "content_type": "application/pdf",
    }
