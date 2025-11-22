"""
Integration tests for authentication endpoints.
"""
import pytest
from httpx import AsyncClient


class TestAuth:
    """Test authentication flows."""

    @pytest.mark.asyncio
    async def test_register_success(self, async_client: AsyncClient, test_user_data):
        """Test successful user registration."""
        response = await async_client.post(
            "/api/v1/auth/register",
            json=test_user_data,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] > 0
        assert data["email"] == test_user_data["email"]

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, async_client: AsyncClient, test_user_data):
        """Test registration with duplicate email."""
        # First registration
        await async_client.post("/api/v1/auth/register", json=test_user_data)

        # Second registration with same email
        response = await async_client.post(
            "/api/v1/auth/register",
            json=test_user_data,
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_success(self, async_client: AsyncClient, test_user_data):
        """Test successful login."""
        # Register first
        await async_client.post("/api/v1/auth/register", json=test_user_data)

        # Login
        response = await async_client.post(
            "/api/v1/auth/login",
            json=test_user_data,
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, async_client: AsyncClient, test_user_data):
        """Test login with invalid credentials."""
        # Register first
        await async_client.post("/api/v1/auth/register", json=test_user_data)

        # Login with wrong password
        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user_data["email"],
                "password": "WrongPassword123!",
            },
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, async_client: AsyncClient):
        """Test login with non-existent user."""
        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePassword123!",
            },
        )
        assert response.status_code == 401
