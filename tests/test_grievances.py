"""
Integration tests for grievance endpoints.
"""
import pytest
from httpx import AsyncClient


class TestGrievances:
    """Test grievance management flows."""

    @pytest.mark.asyncio
    async def test_create_grievance_success(
        self,
        async_client: AsyncClient,
        test_user_data,
        test_grievance_data,
    ):
        """Test successful grievance creation."""
        # Register and login
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        # Create grievance
        response = await async_client.post(
            "/api/v1/grievances",
            json=test_grievance_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == test_grievance_data["title"]
        assert data["status"] == "submitted"
        assert data["id"] > 0

    @pytest.mark.asyncio
    async def test_create_grievance_unauthorized(
        self,
        async_client: AsyncClient,
        test_grievance_data,
    ):
        """Test creating grievance without authentication."""
        response = await async_client.post(
            "/api/v1/grievances",
            json=test_grievance_data,
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_grievance_success(
        self,
        async_client: AsyncClient,
        test_user_data,
        test_grievance_data,
    ):
        """Test retrieving a grievance."""
        # Setup: register, login, create grievance
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        create_response = await async_client.post(
            "/api/v1/grievances",
            json=test_grievance_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        grievance_id = create_response.json()["id"]

        # Retrieve grievance
        response = await async_client.get(
            f"/api/v1/grievances/{grievance_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == grievance_id
        assert data["title"] == test_grievance_data["title"]

    @pytest.mark.asyncio
    async def test_get_nonexistent_grievance(
        self,
        async_client: AsyncClient,
        test_user_data,
    ):
        """Test retrieving non-existent grievance."""
        # Register and login
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        # Try to get non-existent grievance
        response = await async_client.get(
            "/api/v1/grievances/999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_grievance_status(
        self,
        async_client: AsyncClient,
        test_user_data,
        test_grievance_data,
    ):
        """Test updating grievance status."""
        # Setup
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        create_response = await async_client.post(
            "/api/v1/grievances",
            json=test_grievance_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        grievance_id = create_response.json()["id"]

        # Update status
        response = await async_client.patch(
            f"/api/v1/grievances/{grievance_id}",
            json={"status": "under_review"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "under_review"

    @pytest.mark.asyncio
    async def test_resolve_grievance(
        self,
        async_client: AsyncClient,
        test_user_data,
        test_grievance_data,
    ):
        """Test resolving a grievance."""
        # Setup
        await async_client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await async_client.post("/api/v1/auth/login", json=test_user_data)
        token = login_response.json()["access_token"]

        create_response = await async_client.post(
            "/api/v1/grievances",
            json=test_grievance_data,
            headers={"Authorization": f"Bearer {token}"},
        )
        grievance_id = create_response.json()["id"]

        # Resolve
        response = await async_client.post(
            f"/api/v1/grievances/{grievance_id}/resolve",
            json={"resolution": "Issue has been fixed"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "resolved"
